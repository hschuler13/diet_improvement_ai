import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Recipe Generator", page_icon="🍳", layout="wide")
#da css for styling the this page, such as navbar, buttons 
st.markdown("""
            <style>
            .stApp {
                background-color: #f4fff8;
            } 

            div[data-testid="stButton"] {
                border-radius: 6px; 
                background: #861657 !important; 
                color: #ffffff !important;
                font-weight: 500;
                transition: all 0.2s ease;
                width: 100%;  
                white-space: nowrap;  
            }

            div[data-testid="stButton"]>button:hover {
                background-color: #861657 !important;
                color: white !important;
            }

            div[data-testid="stCheckbox"] p {
                color: black !important;
                font-weight: 400;
            }

            .stSlider label {
                color: black !important;
                font-weight: 600;
            }

            .stSlider>div>div>div>div {
                background-color: black !important;
            }
            
             .form-label {
                color: #011638 !important;
                font-weight: 600;
                margin-bottom: 5px;
            }
            
            .stAlert {
                background-color: #011638 !important;
            color: white !important;
            }

            .stAlert>div>div>p {
                color: black !important;
            }
            
            </style>
            """, unsafe_allow_html=True)
#da routing logic
if 'page' not in st.session_state:
    st.session_state.page = "recipe"

btn1, btn2, homebtn, btn3 = st.columns([0.4, 0.4, 2.3, 0.4]) 
with homebtn:
    if st.button("Home", key="home_nav", help="Go back to the home page!"):
        st.switch_page("pages/1_home.py") 
with btn1:
    if st.button("Recipe Helper", key="recipe_nav", help="Go to the recipe generator page!"):
        st.switch_page("pages/3_recipe_generator.py")
with btn2:
    if st.button("Meal Planner", key="meal_nav", help="Go to the meal planner page!"):
        st.switch_page("pages/4_meal_planner.py")
with btn3:
    if st.button("My Profile", key="profile_nav", help="Go to your profile page!"):
        st.switch_page("pages/0_userprofile.py")

st.markdown("""
    <style> [data-testid="stHorizontalBlock"]:has(button[aria-label*="Navigate"]) {
        display: none;}
    </style>
""", unsafe_allow_html=True)

st.divider()

if st.session_state.page != "recipe":
    st.stop()
# da Header title
st.markdown("<h1 style='text-align: center; margin-top: 5px; margin-bottom: 5px; color: #861657'> Create Your Personalized & Powerul Recipes Here!</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; margin-top: 0px; color: #aa4465'> Powered by Claude..</h2>", unsafe_allow_html=True) 
st.markdown("<br>", unsafe_allow_html=True)
#add and save buttons :p
buttoncol2, spacer = st.columns([0.9,7]) 

with buttoncol2: 
    save_btn = st.button("Saved Recipes", key="save_btn")
# upload recipe title 
with st.container(border=True):
    st.markdown("<p class='form-label' <p style='color: #011638; font-weight: 600;'> Recipe Title</p>", unsafe_allow_html=True)   
    widthTitle , _ = st.columns([2, 3]) 
    with widthTitle: 
        recipeTitle = st.text_input("Title", key="recipe_name", max_chars=100, label_visibility="collapsed")
    st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

#recipe upload text or img form! 
    col_text, col_divider, col_image = st.columns([2,0.3,1.2])
    with col_text: 
        st.markdown("<p class='form-label'>Upload your Recipe!</p>", unsafe_allow_html=True)
        recipe_text = st.text_area("Enter your Recipe here", placeholder="Enter your recipe instructions and ingredients here...", key="recipe_instructions", height=220, 
        label_visibility = "collapsed") 

    with col_divider: 
        st.markdown("""<div style='display: flex; justify-content: center; align-items: center; height: 220px;'>
                    <p style='font-size: 18px; color: #999;'>Or</p>
                    </div>""", unsafe_allow_html=True) 
    with col_image: 
        st.markdown("<p class='form-label'>Upload an image of your recipe here..</p>", unsafe_allow_html=True)
        img = st.file_uploader("Upload your recipe image", type=["jpg", "jpeg", "png"], label_visibility = "collapsed")

        if img:
            st.image(img, width=150)
            st.success("Image uploaded successfully!")
    
with st.container(border=True):
#title of modifications section!!
    st.markdown("<p class='form-label'> Enter your desired modifications! </p>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
#budget slider and checkbox :D
    budgetcol, sliderbar = st.columns([1,2])
    with budgetcol: 
        budgetyes = st.checkbox("Budget", value=False, key="budgetbox")
    with sliderbar:
        if budgetyes:
            budgetPrice = st.slider("Select your budget range", min_value= 1, max_value= 1000, value = 50, step= 5, key="budgetslider")
        else:
            budgetPrice = None
    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

    nutritionbtn = st.checkbox("Increased Nutrition Value in Meal", value=False, key="nutritionbox")
    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

#additional dietary restrictions box heheh
    additionalinfo, _ = st.columns([2, 3])
    with additionalinfo: 
        additionalInfo_yes = st.checkbox("Additional Dietary Restrictions or Preferences (eg. allergies, dietary requirements)",  value=False, key="additionalinfobox")
        if additionalInfo_yes: 
            additionalInfoText = st.text_area("Enter any additional dietary restrictions or preferences here!", 
                placeholder="E.g. I'm allergic to nuts, or I prefer low-carb meals!", key="additionalinfotext", 
                height=120, label_visibility="collapsed")
        else: 
            additionalInfoText = None

st.markdown("<br>", unsafe_allow_html=True)

#submit button + logic
if 'generate_clicked' not in st.session_state:
    st.session_state.generate_clicked = False   

submitcol1, submitcol2, submitcol3 = st.columns([1.2, 1, 5]) 
with submitcol1: 
    subtmit_btn = st.button("Generate Recipe!", key="submit", use_container_width=True)


if subtmit_btn: 
    if recipeTitle and (recipeTitle or img):
        st.success("Recipe processing...")
        st.info(f"Recipe: {recipeTitle}")
        st.session_state.generate_clicked = True
        if budgetyes:
            st.info(f"Budget: ${budgetPrice}") 
        if nutritionbtn:
            st.info("Increased Nutrition Value in Meal: Yes")
        if additionalInfo_yes and additionalInfoText:
            st.info(f"Additional Dietary Restrictions or Preferences: {additionalInfoText}")
    else: 
        st.warning("Please enter a recipe title & the meal's instructions or an image before submitting.")


with submitcol2: 
    save_logic = recipeTitle and (recipe_text or img)
    save_button = st.button(
        "Save",
        key = "submit_btn",
        use_container_width=True,
        disabled=not  save_logic, 
        help= "Add a title and either recipe instructions or an image to save the recipe!"  if not save_logic else "Save your recipe!"
    )

if save_button:
    st.success(f"Saved your recipe '{recipeTitle}'!")

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("backend integration placeholde")