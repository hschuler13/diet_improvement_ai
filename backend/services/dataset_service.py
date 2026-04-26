import re
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

agentGoal = "You are a helpful assistant that responds to users' questions about food and nutrition. You can provide information about recipes, ingredients, and dietary advice. Always be friendly and informative in your responses. You will be given recipe data from a dataset, and you should use that data to answer user questions about recipes, ingredients, and nutrition. If you don't know the answer to a question, it's okay to say you don't know. Tell the user to rephrase their response as needed. Your main goal is to help users with their food-related questions. If the user talks about something off topic from this, politely refuse and redirect their response to something topical."

messages = [{"role": "system", "content": agentGoal}]

print("start kimi client, type 'exit' to exit")

while True:
    userInput = input("User: ")

    if userInput.lower() == "exit":
        print("exit kimi client")
        break

    messages.append({"role": "user", "content": userInput})

    # somewhere in here, search thru recipe csv for the top 10 recipes
    # add that to message of the user with a prompt attached (base the given recipe for the response on csv data)
    # NOTE: work on formatting response

    completion = client.chat.completions.create(
        model="moonshotai/Kimi-K2.6:novita",
        messages = messages
    )

    response = completion.choices[0].message
    print("Kimi: " + response.content)

    messages.append({"role": "assistant", "content": response.content})