import os
import feedparser
import urllib.parse

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

        html += "<li>"
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
