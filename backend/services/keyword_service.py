import re
import pandas as pd

# load data
recipes = pd.read_csv("backend/services/data/new_data/NEW_recipes.csv")
nutrition = pd.read_csv("backend/services/data/new_data/NEW_nutrition.csv")

# stopwords
stopwords = {
    "i","me","my","myself","we","our","ours","ourselves",
    "you","your","yours","yourself","yourselves",
    "he","him","his","himself","she","her","hers","herself",
    "it","its","itself","they","them","their","theirs","themselves",
    "what","which","who","whom","this","that","these","those",
    "am","is","are","the","a","an","and","or","but"
}

# only use keywords relevant to recipes
def extract_keywords(query):
    words = re.findall(r'\b\w+\b', query.lower())
    return [w for w in words if w not in stopwords]

# score recipes based on relevance to keywords
def score_recipe(row, keywords):
    text = f"{row['name']} {row['ingredients']}".lower()
    score = 0
    for word in keywords:
        if word in text:
            score += 1
    return score

# perform search through recipe dataset
def search_recipes(query, df):
    keywords = extract_keywords(query)

    df = df.copy()

    # score each recipe
    df["score"] = df.apply(lambda row: score_recipe(row, keywords), axis=1)

    # remove recipes w/ zero matches
    df = df[df["score"] > 0]

    # sort by best match
    df = df.sort_values(by="score", ascending=False)

    # return top 10 matches
    return df.head(10)