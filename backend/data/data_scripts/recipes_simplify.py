import re
import pandas as pd

# load data
recipes = pd.read_csv("RAW_recipes.csv")
interactions = pd.read_csv("RAW_interactions.csv")

# keep needed columns
recipes = recipes[['id', 'name', 'minutes', 'ingredients', 'n_ingredients', 'steps', 'n_steps']]

# filter rows through removing recipes with too few or too many ingredients, steps, or too short or too long cooking times
recipes = recipes[
    (recipes.n_ingredients.between(4, 15)) &
    (recipes.n_steps.between(4, 20)) &
    (recipes.minutes.between(10, 60))
]

# combine rating data for each recipe
ratings_agg = interactions.groupby('recipe_id').agg(
    n_ratings=('rating', 'count'),
    avg_rating=('rating', 'mean')
).reset_index()

# merge both files so the recipes and ratings are all together
df = recipes.merge(ratings_agg, left_on='id', right_on='recipe_id', how='left')

# fill in missing rating information w/ 0s
df['n_ratings'] = df['n_ratings'].fillna(0)
df['avg_rating'] = df['avg_rating'].fillna(0)

# keep recipes that have 5+ ratings (tested) and a rating of 4+ (yummy)
df = df[
    (df.n_ratings >= 5) &
    (df.avg_rating >= 4.0)
]

# normalize recipe names
def normalize_name(name):
    name = str(name).lower()
    name = re.sub(r'[^a-z0-9\s]', '', name)
    name = re.sub(r'\b(best|easy|quick|ultimate|recipe|homemade)\b', '', name)
    return re.sub(r'\s+', ' ', name).strip()
df['norm_name'] = df['name'].apply(normalize_name,)

# drop duplicate recipe names, keep best rated of duplicates
df = df.sort_values(['avg_rating', 'n_ratings'], ascending=False)
df = df.drop_duplicates(subset='norm_name')
df['score'] = df['avg_rating'] * df['n_ratings']
df = df.sort_values('score', ascending=False)

# hard limit to top 30k recipes
df = df.head(30000)

# remove unecessary columns (only needed for .csv merging and organizing)
df = df.drop(columns=['norm_name', 'recipe_id'])

# save new file
df.to_csv("NEW_recipes.csv", index=False)