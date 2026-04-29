import streamlit as st

st.set_page_config(
    page_title="User Profile",
    page_icon="🏠",
)

page_0 = st.Page("pages/0_userprofile.py", title="User Profile", icon="🏠")
page_1 = st.Page("pages/1_recipe_generator.py", title="Recipe Generator", icon="🧑🏻‍🍳")

pg = st.navigation([page_0, page_1])

# Run the selected page
pg.run()