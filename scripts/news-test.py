import feedparser
from datetime import datetime

# CNBC Business News RSS Feed URL
RSS_FEED_URL = "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10001147"

# Parse the RSS feed
feed = feedparser.parse(RSS_FEED_URL)

# Start building the HTML content
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Top Business News</title>
    <style>
        body {
            font-family: garamond, sans-serif;
            line-height: 1.4;
            margin: 15px;
            padding: 0;
        }
        h2 {
            font-weight: bold;
            text-align: left;
        }
        a {
            color: green;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        ul {
            padding: 0;
            list-style: none;
        }
        li {
            margin-bottom: 30px;
        }
        p {
            margin: 0;
            font-size: 16px;
        }
        h3 {
            font-size: 16px;
            font-weight: normal;
        }
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div id="news-section">
        <h2>Top Business News</h2>
        <ul>
"""

# Loop through the articles and add them to the HTML
for entry in feed.entries[:15]:  # Fetch the latest 15 articles
    # Attempt to extract the image URL if available
    image_url = None
    if "media_content" in entry:
        image_url = entry.media_content[0].get("url")
    elif "links" in entry:
        for link in entry.links:
            if link.rel == "enclosure" and link.type.startswith("image/"):
                image_url = link.href
                break

    # Add the article to the HTML, including the image if available
    html_content += f"""
        <li>
            {"<img src='" + image_url + "' alt='Article Image'>" if image_url else ""}
            <h3>
                <a href="{entry.link}" target="_blank" rel="noopener noreferrer"><b>{entry.title}</b></a>
                <p><i>Source:</i> CNBC</p>
            </h3>
            <p>{entry.summary}</p>
        </li>
    """

# Close the HTML structure
html_content += """
        </ul>
    </div>
</body>
</html>
"""

# Save the HTML file
output_file = "news.html"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(html_content)

print(f"{output_file} has been updated with the latest news from CNBC.")
