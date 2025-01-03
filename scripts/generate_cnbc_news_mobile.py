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
            margin-bottom: 15px;
        }
        p {
            margin: 0;
            font-size: 16px;
        }
        h3 {
            font-size: 16px;
            font-weight: normal;
        }

	@media (max-width: 729px) {
                        
    	.mobile-menu {
                display: flex;
                justify-content: space-around;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                background-color: #f4f4f4;
                border-bottom: 1px solid #ccc;
                z-index: 1000;
                padding: 10px 0;
            }
            .mobile-menu button {
                flex: 1;
                padding: 10px;
                font-size: 16px;
                border: none;
                background-color: #fff;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            .mobile-menu button:hover {
                background-color: #e0e0e0;
            }
            body {
                margin-top: 50px; /* Prevent content overlap with the fixed menu */
            }
	}

footer{
	padding:var(--std_padding);
	box-shadow:rgb(0 0 0 / 8%) 0 -1px 0;
	text-align:center;
	color:#717171;font-size:.75em}

@media(min-width:730px){

.mobile-menu {
        display: none;
    }

footer{
	display: none;
    }
}

    </style>
</head>


<body>

<div class="mobile-menu">
    <img src="/static/images/logo.jpg" alt="Real CPI Logo" height="20" />
    <a href="https://www.realcpi.org"><button id="data-button">Data</button></a>
    <a href="https://www.realcpi.org/news.html"><button id="news-button">News</button></a>
</div>
<br>
    <div id="news-section">
        <h2>Top Business News</h2>
        <ul>
"""

# Loop through the articles and add them to the HTML
for entry in feed.entries[:10]:  # Fetch the latest 10 articles
    html_content += f"""
        <li>
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

<footer>
This information is provided for informational purposes only. This is not for advice.
<br><br>
Please let us know if you have any suggestions, including data series or metrics we could add to Real CPI.
<br><br>
Copyright © 2024
&nbsp;
&nbsp;
&nbsp;
&nbsp;
<a href="mailto:contact@realcpi.org">contact@realcpi.org</a>
</footer>

</body>
</html>
"""

# Save the HTML file
output_file = "news.html"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(html_content)

print(f"{output_file} has been updated with the latest news from CNBC.")