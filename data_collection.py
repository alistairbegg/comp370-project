import http.client
import urllib.parse
import json
import time
import os

# define key and search terms 
API_KEY = "PXvKQ6bbIFJXfiwWkGen7UDtwgX2AhTMRq5lnMvl"
KEY_WORD = "Zohran Mamdani"

# open previously collected articles 
if os.path.exists("articles.json"):
    with open("articles.json", 'r', encoding='utf-8') as f:
        articles = json.load(f)
else: # create empty list for articles
    articles = []

# open previously collected article IDs
if os.path.exists("article_ids.json"):
    with open("article_ids.json", 'r', encoding='utf-8') as f:
        article_ids = json.load(f)
else: # create empty list for article IDs 
    article_ids = []

# open saved page from previous requests
if os.path.exists("page.json"):
    with open("page.json", 'r', encoding='utf-8') as f:
        last_page = json.load(f)
else: # create last_page variable
    last_page = 0

page = last_page + 1
requests = 0

while len(articles) < 500 and requests < 100:
    params = urllib.parse.urlencode({
        'api_token': API_KEY,
        'search': KEY_WORD,
        'limit': 3,
        'locale': "us,ca,mx",
        'language': 'en',
        'page' : page,
    })

    # open a secure connection to the news api
    conn = http.client.HTTPSConnection('api.thenewsapi.com')

    # send request to specified endpoint
    conn.request('GET', '/v1/news/all?{}'.format(params))

    res = conn.getresponse()

    # to view status (if any errors occur)
    print("Status:", res.status)

    data = res.read().decode('utf-8')
    conn.close()

    if res.status != 200:
        print("Error returned. Stopping.")
        break

    response_json = json.loads(data)

    new_articles = response_json.get("data", [])
    
    for article in new_articles:
        article_id = article.get("uuid")
        if article_id not in article_ids:
            article_ids.append(article_id)
            articles.append(article)

    page = page+1
    requests = requests+1
    time.sleep(0.3)

# save articles, article IDs, and last page to json files
with open("articles.json", 'w', encoding = 'utf-8') as f:
    json.dump(articles, f, indent=2)

with open("article_ids.json", 'w', encoding='utf-8') as f:
    json.dump(article_ids, f, indent=2)

with open("page.json", 'w', encoding='utf-8') as f:
    json.dump(page, f, indent=2)

