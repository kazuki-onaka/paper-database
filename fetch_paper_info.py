import requests
import time
import json
from scholarly import scholarly

def search_paper_on_scholar(title):
    """
    Google Scholar で論文タイトルを検索し、著者・発行年・要約を取得する。
    """
    try:
        search_query = scholarly.search_pubs(title)
        paper = next(search_query)  # 最初の検索結果を取得
        
        author = ", ".join([a['name'] for a in paper.get("bib", {}).get("author", [])]) if "author" in paper.get("bib", {}) else "Unknown"
        year = paper.get("bib", {}).get("pub_year", "Unknown")
        summary = paper.get("bib", {}).get("abstract", "No summary available")

        return author, year, summary
    except Exception as e:
        print(f"Google Scholar で取得できませんでした: {e}")
        return "Unknown", "Unknown", "No summary available"

def search_paper_on_crossref(title):
    """
    CrossRef API で論文情報を検索し、著者・発行年・要約を取得する。
    """
    url = f"https://api.crossref.org/works?query={title}"
    headers = {"User-Agent": "PaperFetcher/1.0 (email@example.com)"}  # CrossRef のリクエスト要件を満たすために適当な User-Agent を設定
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if "message" in data and "items" in data["message"] and len(data["message"]["items"]) > 0:
                paper = data["message"]["items"][0]
                author = ", ".join([a["family"] + " " + a["given"] for a in paper.get("author", [])]) if "author" in paper else "Unknown"
                year = str(paper.get("published-print", {}).get("date-parts", [[0]])[0][0]) if "published-print" in paper else "Unknown"
                summary = paper.get("abstract", "No summary available")

                return author, year, summary
    except Exception as e:
        print(f"CrossRef で取得できませんでした: {e}")

    return "Unknown", "Unknown", "No summary available"

def get_paper_info(title):
    """
    Google Scholar → CrossRef の順で検索し、著者・発行年・要約を取得する。
    """
    author, year, summary = search_paper_on_scholar(title)
    if author == "Unknown" or year == "Unknown":
        print(f"Google Scholar で見つからなかったため、CrossRef を試行します: {title}")
        author, year, summary = search_paper_on_crossref(title)

    return author, year, summary