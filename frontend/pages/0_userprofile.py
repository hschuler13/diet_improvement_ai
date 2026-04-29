import streamlit as st
from backend.services.dataset_service import ask_kimi

# initiate form
form = st.form("userProfileForm")

# form questions
q1 = form.slider("1. What is your budget per week for groceries?", 0, 300)
q2 = form.slider("2. How far is the closest grocery store from your house (in miles)?", 0.0, 10.0)
q3 = form.slider("3. How many people do you have to cook for?", 0, 10)
q4 = form.multiselect(
    "4. Where do you get groceries from",
    ["traditional grocery store", "wholesale/ bulk store", "corner/ convenience store", "specialty store", "farmer's market/ local businesess", "online - pickup at store", "online - deliver to home", "food pantry", "other"],
)
q5 = form.text_area("5. Do you have any circumstances or conditions that limit your access to groceries or your ability to cook?")
q6 = form.text_input("6. What do you value most in a meal?")
q7 = form.selectbox(
    "7. What is your personal comfort level with cooking?",
    ("No experience", "Beginner", "Intermediate", "Advanced", "Professional"),
)
q8 = form.slider("8. How much time are you able to spend cooking each week (in hours)?", 0, 20)
q9 = form.text_area("9. What are your health goals?")
q10 = form.text_area("10. What food allergies, restrictions or sensitivities have to be taken into consideration?")
q11 = form.text_input("11. What types of cuisine do you prefer?")
q12 =  form.text_area("12. What other considerations should be taken into account when creating nutrition & diet recommendations for you?")
q14 = form.text_area("13. What is your zip code?")

# form submit
submitForm = form.form_submit_button("Submit")

# store submitted data
if submitForm:
    st.session_state.user_profile = {
        "budget": q1,
        "store_distance": q2,
        "people_amount": q3,
        "grocery_sources": q4,
        "profile_allergies": q5,
        "meal_values": q6,
        "cooking_level": q7,
        "weekly_cooking_time": q8,
        "health_goals": q9,
        "allergies": q10,
        "preferred_cuisine": q11,
        "extra_notes": q12
    }



    st.success("user profile form submitted")