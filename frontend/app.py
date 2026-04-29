import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

page_0 = st.Page("pages/0_userprofile.py", title="User Profile", icon="🏠")
page_1 = st.Page("pages/1_home.py", title="Home", icon="🌽")
page_2 = st.Page("pages/2_saved_recipes.py", title="Saved Recipes", icon="🥪")
page_3 = st.Page("pages/3_recipe_generator.py", title="Recipe Generator", icon="🧑🏻‍🍳")

pg = st.navigation([page_0, page_1, page_2, page_3])

# Run the selected page
pg.run()