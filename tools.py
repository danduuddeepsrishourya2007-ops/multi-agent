from ddgs import DDGS

def web_search(query: str, max_results: int = 5) -> str:
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
    if not results:
        return "No results found."
    output = ""
    for r in results:
        output += f"Title: {r['title']}\n"
        output += f"Summary: {r['body']}\n\n"
    return output.strip()