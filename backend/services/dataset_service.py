import os
from dotenv import load_dotenv
from openai import OpenAI
from keyword_service import search_recipes, recipes

load_dotenv()

# connect w/ HuggingFace token
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

# change length of history
MAX_HISTORY = 6  
# store chat history 
chat_history = []

# prompt for Kimi
system_message = {
    "role": "system",
    "content": """
    You are a smart food and nutrition assistant.

    Your job:
    - Recommend recipes based on the provided dataset.
    - Remember recent conversation context.
    - If user says things like:
    "more like that"
    "lower calorie"
    "cheaper"
    "another option"
    then use recent conversation history.

    Be concise, helpful, and natural.

    {insert user profile information}
    """
}



# start 
print("Start recipe AI (type 'exit' to quit)\n")

while True:
    userInput = input("User: ")

    if userInput.lower() == "exit":
        print("Exiting. Farewell!")
        break

    # perform dataset
    results = search_recipes(userInput, recipes)

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

    # user's request
    prompt = f"""
    User Request:
    {userInput}

    Relevant Recipes:
    {dataset_context}

    Use recent conversation context if useful.
    Use only provided recipes when recommending.
    """

    messages = [system_message]

    # include recent memory only
    messages.extend(chat_history[-MAX_HISTORY:])

    # add current user prompt
    messages.append({
        "role": "user",
        "content": prompt
    })

    # call Kimi
    try:
        completion = client.chat.completions.create(
            model="moonshotai/Kimi-K2.6:novita",
            messages=messages,
            temperature=0.7
        )

        response = completion.choices[0].message.content

        print("\n Kimi:", response, "\n")

        # save chat memory
        chat_history.append({
            "role": "user",
            "content": userInput
        })

        chat_history.append({
            "role": "assistant",
            "content": response
        })

        # trim memory if too large
        chat_history = chat_history[-MAX_HISTORY:]

    except Exception as e:
        print(" Error:", e)