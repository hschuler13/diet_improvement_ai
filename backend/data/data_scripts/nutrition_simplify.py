import pandas as pd

# load data
foodGroup1 = pd.read_csv("FOOD-DATA-GROUP1.csv", index_col=0)
foodGroup2 = pd.read_csv("FOOD-DATA-GROUP2.csv", index_col=0)
foodGroup3 = pd.read_csv("FOOD-DATA-GROUP3.csv", index_col=0)
foodGroup4 = pd.read_csv("FOOD-DATA-GROUP4.csv", index_col=0)
foodGroup5 = pd.read_csv("FOOD-DATA-GROUP5.csv", index_col=0)

# merge all 5 files
df = pd.concat([foodGroup1, foodGroup2, foodGroup3, foodGroup4, foodGroup5])

# remove unecessary columns
df = df.drop(columns=['Unnamed: 0', 'Nutrition Density'])

# save new file
df.to_csv("NEW_nutrition.csv", index=False)