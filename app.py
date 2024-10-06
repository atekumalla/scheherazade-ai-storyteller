import os
from dotenv import load_dotenv
import chainlit as cl
import openai
import asyncio
import json
from datetime import datetime
from prompts import SYSTEM_PROMPT
from prompts import IMAGE_GENERATION_PROMPT

from langsmith.wrappers import wrap_openai
from langsmith import traceable
from types import SimpleNamespace
from text_to_image_interface import get_storybook_illustration


# Load environment variables
load_dotenv()

configurations = {
    "mistral_7B_instruct": {
        "endpoint_url": os.getenv("MISTRAL_7B_INSTRUCT_ENDPOINT"),
        "api_key": os.getenv("RUNPOD_API_KEY"),
        "model": "mistralai/Mistral-7B-Instruct-v0.2"
    },
    "mistral_7B": {
        "endpoint_url": os.getenv("MISTRAL_7B_ENDPOINT"),
        "api_key": os.getenv("RUNPOD_API_KEY"),
        "model": "mistralai/Mistral-7B-v0.1"
    },
    "openai_gpt-4": {
        "endpoint_url": os.getenv("OPENAI_ENDPOINT"),
        "api_key": os.getenv("OPENAI_API_KEY"),
        "model": "gpt-4"
    }
}

# Choose configuration
config_key = "openai_gpt-4"
# config_key = "mistral_7B_instruct"
# config_key = "mistral_7B"

# Get selected configuration
config = configurations[config_key]

debug = False
# Initialize the OpenAI async client
client = wrap_openai(openai.AsyncClient(api_key=config["api_key"], base_url=config["endpoint_url"]))

gen_kwargs = {
    "model": config["model"],
    "temperature": 0.3,
    "max_tokens": 5000
}

# Configuration setting to enable or disable the system prompt
ENABLE_SYSTEM_PROMPT = True

@traceable
def get_latest_user_message(message_history):
    # Iterate through the message history in reverse to find the last user message
    for message in reversed(message_history):
        if message['role'] == 'user':
            return message['content']
    return None

@traceable
@cl.on_chat_start
def on_chat_start():    
    message_history = [{"role": "system", "content": SYSTEM_PROMPT+ IMAGE_GENERATION_PROMPT}]
    cl.user_session.set("message_history", message_history)

@traceable
async def generate_response(client, message_history, gen_kwargs):
    response_message = cl.Message(content="")
    await response_message.send()

    stream = await client.chat.completions.create(messages=message_history, stream=True, **gen_kwargs)
    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await response_message.stream_token(token)
    
    await response_message.update()

    return response_message


@traceable
@cl.on_message
async def on_message(message: cl.Message):
    message_history = cl.user_session.get("message_history", [])
    message_history.append({"role": "user", "content": message.content})
    if debug:
        print("Message history:")
        print(message_history)
    response_message = await generate_response(client, message_history, gen_kwargs)
    if debug:
        print("Response message content:")
        print(response_message.content)
    while True:
        if "get_storybook_illustration" in response_message.content:
            # Avoid adding the response_message to the message_history in this case as it is increasing the message size to the OPENAI API
            x = json.loads(response_message.content, object_hook=lambda d: SimpleNamespace(**d))
            # Call the function
            get_storybook_illustration(x.arguments.title, x.arguments.characters, x.arguments.cover_picture_description, x.arguments.num_pages, x.arguments.pages)
            break
        else:
            message_history.append({"role": "assistant", "content": response_message.content})
            break
    
    # response_message = await generate_response(client, message_history, gen_kwargs)
    if debug:
        print("Message history:")
        print(message_history)
    cl.user_session.set("message_history", message_history)


if __name__ == "__main__":
    cl.main()
