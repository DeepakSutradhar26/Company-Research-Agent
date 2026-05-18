import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

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
def llm_report(scraped_text: str, wiki_content: str):
    try:
        parser = PydanticOutputParser(pydantic_object=LeadResponse)

        template = PromptTemplate(
            template="""You are a senior business analyst preparing a personalized company intelligence report for a prospect who just submitted a lead form.

        Your goal is to create a highly curated, professional, and insightful report that demonstrates deep understanding of their business.

        Use the following data sources:
        - Website Content: {scraped_text}
        - Wikipedia / Public Info: {wiki_content}

        If either source is empty or insufficient, infer intelligently from the other source or from your own knowledge about the company and its industry.

        Instructions:
        - Tailor every section specifically to this company — no generic filler
        - Identify their core business model, target market, and value proposition
        - Highlight real challenges and opportunities relevant to their domain
        - Use professional business language
        - Be specific, not vague — mention actual products, services, or initiatives if known
        - The report should feel like it was written by a consultant who researched this company thoroughly

        {format_instructions}""",
            input_variables=['scraped_text', 'wiki_content'],
            partial_variables={'format_instructions': parser.get_format_instructions()}
        )

        chain = template | model | parser

        report = chain.invoke({'scraped_text': scraped_text, 'wiki_content': wiki_content})

        return {
            'success': True,
            'report': report
        }
    except Exception as e:
        return {
            'success': False,
            'message': str(e)
        }