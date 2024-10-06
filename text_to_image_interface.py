# this is a placeholder function that will be implemented later
import requests
from dotenv import load_dotenv
import os

load_dotenv()

generation_endpoint = os.getenv("IDEOGRAM_ENDPOINT") + "/generate"

def get_storybook_illustration(title, characters, cover_picture_description, num_pages, pages):
    print("Generating storybook illustration...")
    print(f"Title: {title}")
    print(f"Characters: {characters}")
    print(f"Cover picture description: {cover_picture_description}")
    print(f"Number of pages: {num_pages}")
    print(f"Pages: {pages}")
    print("Storybook illustration generated successfully!")

    all_character_features = ""
    for character in characters:
        character_name = character.character_name
        traits = character.character_traits
        features = character.character_features
        all_character_features += f"Name of {character_name}:\nTraits of {traits}:\nFeatures of {features}:\n"


    COVER_PICTURE_PROMPT = f"""Generate a cover picture for a children's story book using the following prompt: {cover_picture_description}
        Below you will find a description of each characters that you may need to use for the cover picture based on the above description.
        {all_character_features}
    """
    print("\n--->DEBUG: ", COVER_PICTURE_PROMPT)

    headers = {
        "Api-Key": f"{os.getenv("IDEOGRAM_API_KEY")}",
        "Content-Type": "application/json"
    }
    
    payload = { 
        "image_request": {
            "prompt": f"{cover_picture_description}",
            "aspect_ratio": "ASPECT_10_16",
            "model": "V_2",
            "magic_prompt_option": "AUTO"
        } 
    }

    response = requests.post(generation_endpoint, headers=headers, json=payload)

    print(response.json())

    return response.json()
    

    #https://ideogram.ai/assets/image/lossless/response/H78te17kQ62VMi9F9RnwPQ