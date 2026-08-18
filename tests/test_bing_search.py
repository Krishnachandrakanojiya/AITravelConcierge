import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.tools.search import SearchTools


def main():

    search_tool = SearchTools()

    query = "best restaurants in Paris for travelers"

    print("BING SEARCH TEST")
    print("=" * 50)
    print("Search Query:", query)
    print()

    results = search_tool.search_web(query)

    for index, result in enumerate(results, start=1):
        print(f"Result {index}")
        print("Title:", result.get("title"))
        print("URL:", result.get("url"))
        print("Snippet:", result.get("snippet"))
        print("-" * 50)


if __name__ == "__main__":
    main()