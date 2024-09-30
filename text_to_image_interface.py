# this is a placeholder function that will be implemented later
import requests
from dotenv import load_dotenv
import os

load_dotenv()

generation_endpoint = os.getenv("IDEOGRAM_ENDPOINT") + "/generation"
def get_storybook_illustration(title, characters, cover_picture_description, num_pages, pages):
    print("Generating storybook illustration...")
    print(f"Title: {title}")
    print(f"Characters: {characters}")
    print(f"Cover picture description: {cover_picture_description}")
    print(f"Number of pages: {num_pages}")
    print(f"Pages: {pages}")
    print("Storybook illustration generated successfully!")


def generate_cover_picture(title, characters, cover_picture_description):
    COVER_PICTURE_PROMPT = f"Cover picture for {title} with {characters} and following the description: {cover_picture_description}"
    headers = {
        "Api-Key": f"{os.getenv("IDEOGRAM_API_KEY")}",
        "Content-Type": "application/json"
    }
    
    payload = { 
        "image_request": {
            "prompt": f"{COVER_PICTURE_PROMPT}",
            "aspect_ratio": "ASPECT_10_16",
            "model": "V_2",
            "magic_prompt_option": "AUTO"
        } 
    }

    response = requests.post(generation_endpoint, headers=headers, json=payload)

    print(response.json())

    return response.json()