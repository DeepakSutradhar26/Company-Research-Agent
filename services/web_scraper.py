import requests
from bs4 import BeautifulSoup

# The problem I came accross while working with scraped text is that
# Long paragraph text may exhaust LLM tokens
# So I'm using both wikipedia retriver and scraped text
# Then I will create a pipeline to only pass around less than 8k chars to LLM
def scrape_company_data(url: str):
    if url is None:
        return ''

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')

        # Remove unimportant tags
        for tag in soup(['script', 'style']):
            tag.decompose()
            
        content = []

        # Extract text from useful tags
        for tag in soup(['h1', 'h2', 'h3', 'p', 'span', 'li']):
            text = soup.get_text(separator=' ', strip=True)

            content.append(text)

        final_text = '\n'.join(content)

        return {
            'success': True,
            'text': final_text
        }
    except Exception as e:
        return {
            'success':False,
            'message':str(e)
        }
