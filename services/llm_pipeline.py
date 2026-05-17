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
        parser = PydanticOutputParser(pydantic_object=LeadResponse)

        template = PromptTemplate(
            template='Create a report from either from text1 and text2 given or internet text1: {text1} and text2: {text2} as {format_instructions}',
            input_variables=['text1', 'text2'],
            partial_variables={'format_instructions': parser.get_format_instructions()}
        )

        chain = template | model | parser

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