import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load file
df = pd.read_excel("annotations.xlsx")

# Combine title + description
df["text"] = df["title"].fillna("") + " " + df["description"].fillna("")

# Group by topic
topic_docs = df.groupby("Topic")["text"].apply(lambda x: " ".join(x)).to_dict()

# TF-IDF with unigrams + bigrams
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_df=0.85,
    min_df=2,
    ngram_range=(1,2)
)

corpus = list(topic_docs.values())
topics = list(topic_docs.keys())

tfidf_matrix = vectorizer.fit_transform(corpus)
feature_names = vectorizer.get_feature_names_out()

def clean_top_words(words_with_scores):
    """
    Removes unigrams that are already inside strong bigrams.
    Example: keep 'andrew cuomo', drop 'andrew' + 'cuomo'.
    Example: keep 'donald trump', drop 'donald' + 'trump'
    """

    # Extract only bigrams
    bigrams = [w for w, s in words_with_scores if " " in w]

    cleaned = []
    for w, s in words_with_scores:

        # If unigram is part of any selected bigram, skip it
        if " " not in w:
            if any(w in bg for bg in bigrams):
                continue  # skip the unigram

        cleaned.append((w, s))

    return cleaned[:10]  # return only top 10 after cleaning


# Print top 10 cleaned words per topic
for i, topic in enumerate(topics):
    print("\n=== Top words for topic:", topic, "===\n")

    row = tfidf_matrix[i].toarray().flatten()
    top_indices = row.argsort()[::-1][:20]  # collect top 20 before cleaning
    top_words = [(feature_names[idx], row[idx]) for idx in top_indices]

    cleaned_top = clean_top_words(top_words)

    for word, score in cleaned_top:
        print(f"{word}: {score:.4f}")
