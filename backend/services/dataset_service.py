import os
import ast
import re
from dotenv import load_dotenv
from openai import OpenAI
from backend.services.keyword_service import search_recipes, recipes
from backend.services.nutrtion_service import get_ingredients_restrictions, get_protein_heavy_ingredients,  get_fiber_rich_ingredients, get_low_sodium, get_info, get_food_by_nutrient, calculate_total_nutrition

load_dotenv()

# connect w/ Groq key
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# chat memory & agent role
MAX_HISTORY = 6
system_message = {
    "role": "system",
    "content": """
    You are a smart food and nutrition assistant.

    Your job:
    - Recommend recipes based on the provided dataset.
    - Display nutrition information when requested.
    - Suggest places to buy ingredients when asked.
    - Remember recent conversation context.
    - If user says:
    more like that
    lower calorie
    cheaper
    another option

    Use recent conversation history.

    Be concise, helpful, and natural.

    IMPORTANT TO FOLLOW THESE INSTRUCTIONS:
    - Never suggest ingredients that conflicts with user dietary restrictions, aversions or allergies. 
    - Scale recipe portions for the number of people specified by the user.
    - Match recipe complexity to the user's cooking level and user count of people.
    - Stay within user's budget if provided by them.
    """
}

# communicate w/ model
def ask_model(user_input, chat_history, budget=None, nutrition_priority=False, dietary_restrictions=None, health_goals=None, cooking_level=None, people_amount=1):
    # search recipe dataset
    results = search_recipes(user_input, recipes)

    # insert results into prompt
    if results.empty:
        dataset_context = "No matching recipes found."
    else:
        dataset_context = ""

        for _, row in results.iterrows():
            # Parse ingredients - handle both string list format and comma-separated
            raw_ingredients = str(row.get('ingredients', '')).strip()

            clean_str = re.sub(r"[\[\]'\"]", "", raw_ingredients)
            ing_list = [i.strip() for i in clean_str.split(',') if i.strip()]

            totals = calculate_total_nutrition(ing_list)

            dataset_context += f"""
                Recipe Name: {row['name']}
                Ingredients: {row['ingredients']}
                Relevance Score: {row['score']}
                """ 
    safety_context = ""
    if dietary_restrictions:
        safety_context = "User Has These Dietary Restrictions: {dietary_restrictions} Verify that none of these ingredients in the recommended recipes conflict with these restrictions."

            
    nutrition_context = "Nutrition Info for Mentioned Ingredients: \n"
    if nutrition_priority:
        high_protein_foods = get_protein_heavy_ingredients(min_protein=20)
        nutrition_context += "\n Your High-Protein Options:\n"
        for food in high_protein_foods[:5]:  
            nutrition_context += f"- {food.get('food')}: {food.get('Protein')}g protein, {food.get('Caloric Value')} cal\n"

        rich_fiber_foods = get_fiber_rich_ingredients(dietary_fiber=3.0)
        nutrition_context += "\n Your High-Fiber Options:\n"
        for food in rich_fiber_foods[:5]:
            nutrition_context += f"- {food.get('food')}: {food.get('Dietary Fiber')}g dietary fiber, {food.get('Caloric Value')} cal\n"

        sodium_balanced_foods = get_low_sodium(max_sodium=0.3)
        nutrition_context += "\n Your Low-Sodium Options:\n"    
        for food in sodium_balanced_foods[:5]:
            nutrition_context += f"- {food.get('food')}: {food.get('Sodium')}g sodium, {food.get('Caloric Value')} cal\n"

    words = user_input.lower().split()
    for word in words:
        if len(word) > 3:
            info = get_info(word)
            if info:
                nutrition_context += f"- {info.get('food')}: {info.get('Caloric Value')} cal, {info.get('Protein')}g protein, {info.get('Fat')}g fat\n"
        
    if health_goals:
        if "weight" in health_goals.lower():
            vitamin_foods = get_food_by_nutrient("Vitamin C", min_value=0.1)  
            nutrition_context += "Vitamin Rich Ingredient Options for Weight Management:\n"
            for food in vitamin_foods[:3]:
                nutrition_context += f"- {food.get('food')}: Vitamin C {food.get('Vitamin C')}\n"

        if "muscle" in health_goals.lower():
            iron_foods = get_food_by_nutrient("Iron", min_value=0.1)
            nutrition_context += " Iron-Rich Ingredients Options for Muscle Goals:\n"
            for food in iron_foods[:3]:
                nutrition_context += f"- {food.get('food')}: Iron {food.get('Iron')}\n"


    # build prompt 
    prompt = f"""
                User Request:
                {user_input}

                Relevant Recipes:
                {dataset_context}

                Nutrition Priority: {nutrition_context} 

                Nutrition Priority: {'Yes - prioritize high-protein foods' if nutrition_priority else 'No'}

                Relevant Recipes: 
                {dataset_context}

                Important Instructions:
                - Never suggest ingredients that conflicts with user's dietary restrictions/sensitivities/allergies.
                - Scale recipe portions for the number of people specified by the user.
                - Match recipe complexity to the user's cooking level.
                - Stay within user's budget if provided by them.
                - Only recommend recipes from the provided dataset.

                Use recent conversation context to remember user preferences/needs.
                """

    messages = [system_message]
    messages.extend(chat_history[-MAX_HISTORY:])
    messages.append({
        "role": "user",
        "content": prompt
    })

    # communicate w/ model
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.7
    )

    response = completion.choices[0].message.content

    # update chat history
    chat_history.append({
        "role": "user",
        "content": user_input
    })

    chat_history.append({
        "role": "assistant",
        "content": response
    })

    chat_history[:] = chat_history[-MAX_HISTORY:]

    # return response for user
    return response