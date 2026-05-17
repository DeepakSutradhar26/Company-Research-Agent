# Retrivers being runnables, we can call invoke method
from langchain_community.retrievers import WikipediaRetriever

retriver = WikipediaRetriever(top_k_results=1, lang='en')

def search_company_name(company_name: str):
    company_name = company_name.lower()

    try:
        docs = retriver.invoke(company_name)

        return {
            'success': True,
            'text': docs[0].page_content
        }
    except Exception as e:
        return {
            'success': False,
            'message': str(e)
        }
