from langchain.tools import tool
import requests
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from rich import print


load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TVLY_API_KEY"))

@tool()
def web_search(query:str)->str:
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets."""
    result= tavily.search(query=query , max_results=5)

    out= []

    for r in result['results']:
        out.append(f"title:{r['title']}\nURL:{r['url']}\nSnippet:{r['content'][:300]}")

    return '\n---------\n'.join(out)


# print(web_search("Ai news in india"))



@tool()
def scrap_url(url:str)->str:
    """scrap and return the clean text"""

    try:
        resp = requests.get(url=url , timeout=8, headers={"User-Agent":"Mozilla/5.0"})
        soup= BeautifulSoup(resp.text , "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        return soup.get_text(separator=" " , strip=True)[:3000]
    except Exception as e :
        return f"Could not scrap url :{str(e)}"

