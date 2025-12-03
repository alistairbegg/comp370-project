import json
import csv

# Load articles from JSON file
with open('articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

# Extract first 200 articles
articles_subset = articles[:200]

# Write to CSV file
with open('articles_extracted.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    
    # Write header row
    writer.writerow(['uuid', 'title', 'description'])
    
    # Write data rows
    for article in articles_subset:
        uuid = article.get('uuid', '')
        title = article.get('title', '')
        description = article.get('description', '')
        writer.writerow([uuid, title, description])

print(f"Extracted {len(articles_subset)} articles to articles_extracted.csv")
