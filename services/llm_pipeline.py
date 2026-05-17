import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.runnables import RunnableLambda

from schema.response import LeadResponse

load_dotenv()

# Used Groq API since free and easy to use
model = ChatGroq(
    model='llama-3.3-70b-versatile',
    groq_api_key=os.getenv('GROQ_API_KEY'),
    temperature=0,
    timeout=30,
    max_retries=1
)

# Letting LLM first generate a prompt which can be passed to generate the report
def llm_report(text1: str, text2: str):
    try:
        parser1 = StrOutputParser()

        parser2 = PydanticOutputParser(pydantic_object=LeadResponse)

        templat1 = PromptTemplate(
            template="""Find information about this company either from given texts or internet.
            text1: {text1}, text2 {text2}""",
            input_variables=['text1', 'text2']
        )

        template2 = PromptTemplate(
            template='Create a report from information given {text} as {format_instructions}',
            input_variables=['text'],
            partial_variables={'format_instructions': parser2.get_format_instructions()}
        )

        chain = (
            templat1 | 
            model | 
            parser1 | 
            RunnableLambda(lambda x: {'text': x}) | 
            template2 | 
            model | 
            parser2
            )

        report = chain.invoke({'text1': text1, 'text2': text2})

        return {
            'success': True,
            'report': report
        }
    except Exception as e:
        return {
            'success': False,
            'message': str(e)
        }