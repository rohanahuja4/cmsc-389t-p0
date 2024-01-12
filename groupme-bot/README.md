# RohBot

## Summary

RohBot is a GroupMe bot with a number of basic interactive functions. It partially relies on OpenAI's GPT-3.5 API to generate text responses.

## Features/Functionality
The responses produced by RohBot are delivered as messages to the CMSC389T GroupMe chat. There are two categories of responses:

**General Responses**

These responses are triggered when _any_ user sends a message requesting a haiku, one of two greetings (in any letter case), or a nonsensical message:
- If any user asks a message that starts with "haiku " followed by a topic, the bot will respond with a haiku about that topic using the GPT-3.5 API.
- If any user says "good morning" or "good night" (regardless of the letter casing), the bot will respond in kind ("Good morning" or "Good night", respectively), followed by the user's first name.
- If any user says gibberish or a message that does not contain one of the predefined inputs, the bot will respons "I'm sorry, I don't understand. I'm just a bot."

**Personalized Responses to Bot Owner**

These responses are triggered when the _bot owner_ sends a message asking who the bot is:
- If the bot owner sends a message containing the string "who are you?" (regardless of casing), the bot will respond with a witty message tailored to that question.

## How to Run

1. Clone this repository.
2. Change directory to the cloned repository.
3. Create and activate a virtual environment.
4. Run `pip install -r requirements.txt` to install the required dependencies.
5. Change directory to the `groupme-bot` folder.
6. Run `python3 bot.py` to start the bot.