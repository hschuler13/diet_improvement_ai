import os
from dotenv import load_dotenv
from openai import OpenAI
from backend.services.keyword_service import search_recipes, recipes

load_dotenv()

# connect to HuggingFace router
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

# chat memory & agent role
MAX_HISTORY = 6
system_message = {
    "role": "system",
    "content": """
    You are a smart food and nutrition assistant.

    Your job:
    - Recommend recipes based on the provided dataset.
    - Remember recent conversation context.
    - If user says:
    more like that
    lower calorie
    cheaper
    another option

    Use recent conversation history.

    Be concise, helpful, and natural.

    {insert user profile information}
    """
}

# communicate w/ model & 
def ask_kimi(user_input, chat_history):
    # search recipe dataset
    results = search_recipes(user_input, recipes)

    # sort results from dataset search
    if results.empty:
        dataset_context = "No matching recipes found."
    else:
        dataset_context = ""

        for _, row in results.iterrows():
            dataset_context += f"""
                Recipe Name: {row['name']}
                Ingredients: {row['ingredients']}
                Relevance Score: {row['score']}
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
        model="moonshotai/Kimi-K2.6:novita",
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