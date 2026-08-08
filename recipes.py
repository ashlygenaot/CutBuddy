import requests
from bs4 import BeautifulSoup
from strands import tool
from typing import List, Dict, Any


TRUSTED_DOMAINS = {
    "allrecipes.com",
    "eatingwell.com",
    "skinnytaste.com",
    "foodnetwork.com",
    "delish.com",
    "bbcgoodfood.com",
}

def is_recipe_page(url: str, title: str) -> bool:
    """
    Filter out collection pages and keep individual recipes.
    """

    blocked_terms = [
        "ideas",
        "best",
        "top",
        "collection",
        "roundup",
        "list",
        "high-protein",
        "meal-plan"
    ]

    url_lower = url.lower()
    title_lower = title.lower()

    # reject obvious collection pages
    for term in blocked_terms:
        if term in url_lower or term in title_lower:
            return False

    return True

def search_recipes_web(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """Search trusted recipe websites for recipes matching a query."""

    url = "https://html.duckduckgo.com/html/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.post(
            url,
            data={"q": query},
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        
        for item in soup.find_all("div", class_="result")[:max_results]:
            link = item.find("a", class_="result__a")

            if not link:
                continue

            recipe_url = link.get("href", "")
            title = link.get_text(strip=True)

            snippet = item.find("a", class_="result__snippet")
            snippet_text = snippet.get_text(strip=True) if snippet else ""
            if any(domain in recipe_url.lower() for domain in TRUSTED_DOMAINS):
                results.append({
                    "title": title,
                    "url": recipe_url,
                    "snippet": snippet_text
                })

        return results

    except requests.RequestException:
        return []

def collect_recipe_results(ingredients):

    searches = [
        f"{ingredients} breakfast recipe",
        f"chicken rice broccoli recipe",
        f"high protein chicken recipe",
        f"protein snack recipe"
    ]


    results = []

    for query in searches:
        results.extend(search_recipes_web(query))

    return results
