import requests
import time
import json
import os
from openai import OpenAI, api_key
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

BOT_ID = os.getenv("BOT_ID")
GROUP_ID = os.getenv("GROUP_ID")
GROUPME_ACCESS_TOKEN = os.getenv("GROUPME_ACCESS_TOKEN")
LAST_MESSAGE_ID = None


def send_message(text, attachments=None):
    """Send a message to the group using the bot."""
    post_url = "https://api.groupme.com/v3/bots/post"
    data = {"bot_id": BOT_ID, "text": text, "attachments": attachments or []}
    response = requests.post(post_url, json=data)
    return response.status_code == 202


def get_group_messages(since_id=None):
    """Retrieve recent messages from the group."""
    params = {"token": GROUPME_ACCESS_TOKEN}
    if since_id:
        params["since_id"] = since_id

    get_url = f"https://api.groupme.com/v3/groups/{GROUP_ID}/messages"
    response = requests.get(get_url, params=params)
    if response.status_code == 200:
        return response.json().get("response", {}).get("messages", [])
    return []


def process_message(message):
    """Process and respond to a message."""
    global LAST_MESSAGE_ID
    text = message["text"].lower()
    print(f"Processing message: {text} from {message['name']} ({message['sender_id']}))")

    if message["sender_id"] == "9578291" and "who are you?" in text:
        configuration = "Describe yourself (yourself being a GPT) in a concise but tongue-in-cheek manner (e.g., as an omnipotent artificial intelligence or something else funny like that)."
        subject = text
        answer = generate_response(subject, configuration)
        send_message(answer)
    elif message["sender_type"] != "bot":
        if text.startswith("haiku ") and len(text) > 6:
            configuration = "You are a poet who responds only with an elegant haiku about the subject matter requested. If the subject matter is incoherent, write a snarky haiku about the user's lack of clarity. You should be very careful that you choose a 5-7-5 scheme, even if that means you have to keep the haikus exceedingly simple."
            subject = text[6:]
            haiku = generate_response(subject, configuration)
            send_message(haiku)
        else:
                if "good morning" in text:
                    send_message("Good morning " + message["name"].split(" ")[0] + "!")
                elif "good night" in text:
                    send_message("Good night " + message["name"].split(" ")[0] + "!")
                else:
                    send_message("I'm sorry, I don't understand. I'm just a bot.")

    LAST_MESSAGE_ID = get_group_messages()[0]["id"]

def generate_response(text, configuration):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": configuration},
            {"role": "user", "content": text}
        ]
    )

    print(completion)
    return(completion.choices[0].message.content)

def main():
    global LAST_MESSAGE_ID
    messages = get_group_messages()
    LAST_MESSAGE_ID = messages[0]["id"]
    print(f"Last message id: {LAST_MESSAGE_ID}")
    while True:
        print("Checking for new messages...")
        messages = get_group_messages(LAST_MESSAGE_ID)
        for message in reversed(messages):
            process_message(message)
        time.sleep(10)

if __name__ == "__main__":
    main()