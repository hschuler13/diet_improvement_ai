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

# recipes variable declaration
topRecipes = 0

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
    topRecipes = df.head(10)
    return topRecipes

def search_nutrition(query, df):
    # first get top recipe matches
    topRecipes = search_recipes(query, recipes)

    nutrition_results = []

    for _, recipe in topRecipes.iterrows():
        # split ingredients into list
        ingredients = str(recipe["ingredients"]).lower().split(",")

        matched_nutrition = []

        for ingredient in ingredients:
            ingredient = ingredient.strip()

            # search nutrition dataset for ingredient match
            matches = df[
                df["name"].str.lower().str.contains(ingredient, na=False, regex=False)
            ]

            # add matching rows
            for _, match in matches.iterrows():
                matched_nutrition.append({
                    "ingredient": ingredient,
                    "Caloric Value": match.get("Caloric Value", "N/A"),
                    "Protein": match.get("Protein", "N/A"),
                    "Fat": match.get("Fat", "N/A"),
                    "Carbohydrates": match.get("Carbohydrates", "N/A")
                })

        nutrition_results.append({
            "recipe_name": recipe["name"],
            "ingredients": recipe["ingredients"],
            "nutrition_info": matched_nutrition
        })

    return nutrition_results