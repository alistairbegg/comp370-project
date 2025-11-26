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
        article_list = json.load(f)
else: # create empty list for articles
    article_list = []

# open previously collected article IDs
if os.path.exists("article_ids.json"):
    with open("article_ids.json", 'r', encoding='utf-8') as f:
        id_list = json.load(f)
else: # create empty list for article IDs 
    id_list = []

page = 1
requests = 0

while len(article_list) < 500 and requests < 100:
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
    data = res.read().decode('utf-8')
    conn.close()

    response_json = json.loads(data)

    articles = response_json.get("data", [])
    
    for article in articles:
        article_id = article.get("uuid")
        if article_id not in id_list:
            id_list.append(article_id)
            article_list.append(article)

    page = page+1
    requests = requests+1
    time.sleep(0.5)

# save articles and article ids to json files
with open("articles.json", 'w', encoding = 'utf-8') as f:
    json.dump(article_list, f, indent=2)

with open("article_ids.json", 'w', encoding='utf-8') as f:
    json.dump(id_list, f, indent=2)

