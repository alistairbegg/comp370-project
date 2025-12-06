import json
import csv

with open('articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

articles_subset = articles

with open('articles_extracted.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['uuid', 'title', 'description'])
    
    for article in articles_subset:
        uuid = article.get('uuid', '')
        title = article.get('title', '')
        description = article.get('description', '')
        writer.writerow([uuid, title, description])

print(f"Extracted {len(articles_subset)} articles to articles_extracted.csv")
