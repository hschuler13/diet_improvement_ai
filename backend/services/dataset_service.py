import os
from dotenv import load_dotenv
from openai import OpenAI
from backend.services.keyword_service import search_nutrition, recipes

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

    If 

    {insert user profile information}
    """
}

# communicate w/ model
def ask_model(user_input, chat_history):
    results = search_nutrition(user_input, recipes)

    # insert results into prompt
    if not results:
        dataset_context = "No matching recipes found."
    else:
        dataset_context = ""

        for row in results:
            if isinstance(row, dict):
                recipe_name = row.get("recipe_name", "")
                ingredients = row.get("ingredients", "")
                nutrition_info = row.get("nutrition_info", "")
            else:
                recipe_name = row[0] if len(row) > 0 else ""
                ingredients = row[1] if len(row) > 1 else ""
                nutrition_info = row[2] if len(row) > 2 else ""

            dataset_context += f"""
                Recipe Name: {recipe_name}
                Ingredients: {ingredients}
                Nutrition Info: {nutrition_info}
                """

    # build prompt 
    prompt = f"""
                User Request:
                {user_input}

                Relevant Recipes:
                {dataset_context}

                Use recent conversation context if useful.
                Use only provided recipes when recommending.
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