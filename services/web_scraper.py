import re
import requests
from bs4 import BeautifulSoup

# The problem I came accross while working with scraped text is that
# Long paragraph text may exhaust LLM tokens
# So I'm using both wikipedia retriver and scraped text
# Then I will create a pipeline to only pass around less than 8k chars to LLM
def scrape_company_data(url: str, max_words: int = 450):
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
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            tag.decompose()
            
        priority_tags = ['h1', 'h2', 'h3', 'p', 'li', 'span']

        collected, word_count = [], 0

        for tag_name in priority_tags:
            for tag in soup.find_all(tag_name):
                text = tag.get_text(separator=' ', strip=True)
                text = re.sub(r'\s+', ' ', text)  # collapse whitespace

                if len(text) < 20:
                    continue

                words = text.split()
                remaining = max_words - word_count

                if len(words) > remaining:
                    collected.append(' '.join(words[:remaining]))
                    word_count = max_words
                else:
                    collected.append(' '.join(words))
                    word_count += len(words)
            if word_count >= max_words:
                break

        return {
            'success': True,
            'text': '\n'.join(collected),
            'word_count': word_count
        }

    except Exception as e:
        return {
            'success':False,
            'message':str(e)
        }
