import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# Used Groq API since free and easy to use
model = ChatGroq(
    model='llama-3.3-70b-versatile',
    groq_api_key=os.getenv('GROQ_API_KEY'),
    temperature=0,
    timeout=30,
    max_retries=1
)

template = PromptTemplate(
    template=''
)