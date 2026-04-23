import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

messages = [{"role": "system", "content": "You are a useful assistant that responds to users' questions"}]

print("start kimi client, type 'exit' to exit")

while True:
    userInput = input("User: ")

    if userInput.lower() == "exit":
        print("exit kimi client")
        break

    messages.append({"role": "user", "content": userInput})

    completion = client.chat.completions.create(
        model="moonshotai/Kimi-K2.6:novita",
        messages = messages
    )

    response = completion.choices[0].message
    print("Kimi: " + response.content)

    messages.append({"role": "assistant", "content": response.content})
