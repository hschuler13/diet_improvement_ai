import re
import pandas as pd

# NOTE: do i need to put this in like a main function or sum shit bruh? or can i just ball with it
# load data
recipes = pd.read_csv("NEW_recipes.csv")
recipes = pd.read_csv("NEW_nutrition.csv")

# filter out stopwords from user input
stopwords = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are",("theirs")
}

# use keywords to search through recipes & ingredients
# keep the ten best recipes that have the best keyword hits

# return top ten recipes and associated data (in JSON format)

