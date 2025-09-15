import os, re

from crewai.tools import tool
from firecrawl import FirecrawlApp, ScrapeOptions


# @tool
def web_search_tool(query: str):
    app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

    response = app.search(
        query=query,
        limit=5,
        scrape_options=ScrapeOptions(
            formats=["markdown"],
        ),
    )

    if not response.success:
        return "Error using tool."

    cleaned_chunks = []

    for result in response.data:
        title = result["title"]
        url = result["url"]
        markdown = result["markdown"]

        cleaned = re.sub(r"\\+|\n+", "", markdown).split()
        cleaned = re.sub(r"\[[^\]]+\]\([^\)]+\)|https?://[^\s]+", "", cleaned)

        cleaned_result = {
            'title': title,
            'url': url,
            'markdown': cleaned,
        }

        cleaned_chunks.append(cleaned_result)

    return cleaned_chunks

print(web_search_tool("remote jobs in europe rust"))