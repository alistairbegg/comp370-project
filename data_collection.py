import http.client
import urllib.parse
import json
import time

API_KEY = "PXvKQ6bbIFJXfiwWkGen7UDtwgX2AhTMRq5lnMvl"
KEY_WORD = "Zohran Mamdani"

article_list = []

while len(article_list) < 100:
    params = urllib.parse.urlencode({
        'api_token': API_KEY,
        'search': KEY_WORD,
        'limit': 100,
        'locale': "us,ca,mx",
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

    article_list.extend(articles)

    time.sleep(0.5)

# save to json file
with open("zohran_mamdani_articles.json", 'w', encoding = 'utf-8') as f:
    json.dump(article_list, f, indent=2)

