import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

page_0 = st.Page("pages/0_personalization.py", title="Personalization", icon="👤")
page_1 = st.Page("pages/1_ingredient_locator.py", title="Ingredient Locator", icon="🌽")
page_2 = st.Page("pages/2_nutrition_analysis.py", title="Nutrition Analysis", icon="🥪")
page_3 = st.Page("pages/3_recipe_generator.py", title="Recipe Generator", icon="🧑🏻‍🍳")
page_4 = st.Page("pages/4_meal_planner.py", title="Meal Planner", icon="🍽️")

pg = st.navigation([page_0, page_1, page_2, page_3, page_4])

# Run the selected page
pg.run()