import os
import feedparser
import requests
from bs4 import BeautifulSoup
import urllib.parse

def fetch_image_url(article_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(article_url, headers=headers, timeout=5)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.content, "html.parser")
        og_image = soup.find("meta", property="og:image")
        return og_image["content"] if og_image else None
    except:
        return None

def generate_news_html(ticker):
    query = urllib.parse.quote_plus(ticker)
    rss_url = f"https://news.google.com/rss/search?q={query}+stock"

    feed = feedparser.parse(rss_url)
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
    body {{ font-family: Garamond, sans-serif; padding: 15px; line-height: 1.4; }}
    h2 {{ font-size: 20px; }}
    img {{ max-width: 320px; margin-bottom: 10px; display: block; }}
    a {{ text-decoration: none; color: darkgreen; }}
    a:hover {{ text-decoration: underline; }}
    p {{ margin: 0; font-size: 15px; }}
    li {{ margin-bottom: 25px; list-style: none; }}
    </style>
    </head>
    <body>
    <h2>📰 Related News for: {ticker.upper()}</h2>
    <ul>
    """

    for entry in feed.entries[:10]:
        link = entry.link
        title = entry.title
        summary = entry.summary
        image_url = fetch_image_url(link)

        html += "<li>"
        if image_url:
            html += f"<img src='{image_url}' alt='Image'>"
        html += f"<a href='{link}' target='_blank'><b>{title}</b></a>"
        html += f"<p>{summary}</p></li>"

    html += "</ul></body></html>"

    # 🔽 Write to repo root, even if this script is inside /scripts
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    output_path = os.path.join(repo_root, "news_ticker.html")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ news_ticker.html generated at {output_path}")

# Example usage
generate_news_html("AAPL")
