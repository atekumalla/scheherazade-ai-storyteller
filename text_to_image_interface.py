import requests
from dotenv import load_dotenv
import os
import random
from download_image import download_file
from create_pdf import convert_images_to_pdf
from openai import OpenAI
from page_text_to_image import generate_image_from_page_text
from page_text_to_image import merge_images_horizontally
from page_text_to_image import get_random_font
import asyncio
from concurrent.futures import ThreadPoolExecutor

client =  OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_ENDPOINT"))
# Flag to use DallE
usingDallE = False

load_dotenv()

def generate_dalle_image(image_description, character_features, isPage=False):
    if isPage:
        PICTURE_PROMPT = f"""Generate a picture for a page in a children's story book using the following prompt: \n
        {image_description}\n
        Below you will find a description of each characters that you may need to use for the picture based on the above description. \n
        {character_features} \n

        Make sure the image is in a style appropriate for a children's story book.\n
        Do not create this image as a coverpage.\n
        Ensure to use the seed and create and image where all the characters are still the same age and look similar to the seed picture.\n
        Use a crayon cartoon style for the images.
            
        IMPORTANT: Do not have add any text to the image!\n
        """
    else:
        PICTURE_PROMPT = f"""Generate a picture for a children's story book using the following prompt:\n
        {image_description}\n
        Below you will find a description of each characters that you may need to use for the cover picture based on the above description.\n
        {character_features}\n

        Make sure the image is in a style appropriate for a children's story book.\n
        Use a crayon cartoon style for the images.
            
        IMPORTANT: Do not have add any text to the image!\n
        """
    
    print("\n--->DEBUG: ", PICTURE_PROMPT)

    response = client.images.generate(
        model="dall-e-3",
        prompt=PICTURE_PROMPT,
        size="1024x1024",
        quality="standard",
        n=1
    )
    return response


def generate_image(image_description, character_features, isPage ,seed=None):
    if isPage:
        PICTURE_PROMPT = f"""Generate a picture for a page in a children's story book using the following prompt: \n
        {image_description}\n
        Below you will find a description of each characters that you may need to use for the picture based on the above description. \n
        {character_features} \n

        Make sure the image is in a style appropriate for a children's story book.\n
        Do not create this image as a coverpage.\n
        Ensure to use the seed and create and image where all the characters are still the same age and look similar to the seed picture.\n
            
        IMPORTANT: Do not have add any text to the image!\n
        """
    else:
        PICTURE_PROMPT = f"""Generate a picture for a children's story book using the following prompt:\n
        {image_description}\n
        Below you will find a description of each characters that you may need to use for the cover picture based on the above description.\n
        {character_features}\n

        Make sure the image is in a style appropriate for a children's story book.\n
            
        IMPORTANT: Do not have add any text to the image!\n
        """
    
    print("\n--->DEBUG: ", PICTURE_PROMPT)
    print("\n--->INPUT SEED: ", seed)

    generation_endpoint = os.getenv("IDEOGRAM_ENDPOINT") + "/generate"
    print("\n--->DEBUG: Generation endpoint:   ", generation_endpoint)
    headers = {
        "Api-Key": f'{os.getenv("IDEOGRAM_API_KEY")}',
        "Content-Type": "application/json"
    }
    if seed is not None:
        payload = { 
            "image_request": {
                "prompt": f"{PICTURE_PROMPT}",
                "negative_prompt": "not text, no words, no typography, no letters",
                "aspect_ratio": "ASPECT_10_16",
                "model": "V_2",
                "magic_prompt_option": "OFF",
                "style_type": "DESIGN",
                "seed": seed
            } 
        }
    else:
        payload = { 
            "image_request": {
                "prompt": f"{PICTURE_PROMPT}",
                "negative_prompt": "not text, no words, no typography, no letters",
                "aspect_ratio": "ASPECT_10_16",
                "model": "V_2",
                "style_type": "DESIGN",
                "magic_prompt_option": "OFF"
            } 
        }
    print(f"--->DEBUG: Ideogram Payload: {payload}")
    response = requests.post(generation_endpoint, headers=headers, json=payload)
    return response

'''
SAMPLE PROMPTS for TESTING:

1. can you generate a story about and idli and vada going to italy for a 1 year old. Keep the story 3 pages long

2. generate a story about a boy who love firetrucks and ambulances. Make sure the story is appropriate for a 2 year old. Keep it 3 pages long
'''

def get_image_seed(response):
    try:
        # Access the first item in the 'data' list
        data_item = response['data'][0]
        # Extract the seed and convert it to an integer
        seed = int(data_item['seed'])
        return seed
    except (KeyError, IndexError, ValueError):
        # Return None if the seed is not found or cannot be converted to an integer
        print("No seed found in the response.")
        return None

def get_image_url(response):
    if 'data' in response and isinstance(response['data'], list) and len(response['data']) > 0:
        # Extract the URL from the first item in the 'data' list
        image_data = response['data'][0]
        if 'url' in image_data:
            return image_data['url']
    return None

def get_dalle_image_url(response):
    print(f"==> Debug: {response}")
    return response.data[0].url

def get_image_resolution(response):
    if 'data' in response and isinstance(response['data'], list) and len(response['data']) > 0:
        # Extract the Resolution from the first item in the 'data' list
        image_data = response['data'][0]
        if 'resolution' in image_data:
            return image_data['resolution']
    return None

def download_image_from_response(response, filename):
    if usingDallE:
        image_url = get_dalle_image_url(response)
    else:
        image_url = get_image_url(response.json())

    if image_url:
        print(f"---> DEBUG: Image URL: {image_url}")
        download_file(image_url, filename, "images")
    else:
        print("Image URL not found in the response.")

async def generate_cover_page_async(cover_picture_description, all_character_features, title, resolution, random_number):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(
            pool,
            generate_cover_page,
            cover_picture_description,
            all_character_features,
            title,
            resolution,
            random_number
        )

def generate_cover_page(cover_picture_description, all_character_features, title, resolution, random_number):
    print(f"==> Generating cover page")
    # Generating Cover Picture
    if usingDallE:
        response = generate_dalle_image(cover_picture_description, all_character_features, False)
        print(f"---> DEBUG: {response}")
    else:
        response = generate_image(cover_picture_description, all_character_features, False, seed=random_number)
        # print(f"---> DEBUG: {response.json()}")

    download_image_from_response(response, "page_0_image.png")

    if not usingDallE:
        seed = random_number  # get_image_seed(response.json())
        print(f"---> DEBUG: Using Seed: {seed} from the cover image")
        resolution = get_image_resolution(response.json())
        print(f"--->DEBUG: Resolution: {resolution} from the cover image")

    # Generate the cover image text image
    generate_image_from_page_text(title, resolution, "page_0_text_image.png", "images", is_cover=True)

    # Merge the cover image with the combined image
    if merge_images_horizontally("images", "page_0_image.png", "page_0_text_image.png", "page_0_combined_image.png"):
        # delete the cover image and the text image
        os.remove("images/page_0_image.png")
        os.remove("images/page_0_text_image.png")
        print(f"Deleted images/page_0_image.png and images/page_0_text_image.png")
        return True, seed, resolution
    else:
        print("Failed to merge images.")
        return False, None, None

def process_page(page, all_character_features, resolution, page_font, seed):
    print(f"==> Processing page {page.page_num}")
    if usingDallE:
        response = generate_dalle_image(page.page_picture_description, all_character_features, True)
        print(f"---> DEBUG: {response}")
    else:
        response = generate_image(page.page_picture_description, all_character_features, True, seed)
        print(f"--->DEBUG: {response}")
    
    download_image_from_response(response, f"page_{page.page_num}_image.png")
    # Generate the page image text image
    generate_image_from_page_text(page.page_text, resolution, f"page_{page.page_num}_text_image.png", "images", is_cover=False, font_to_use=page_font)
    # Merge the cover image with the combined image
    if merge_images_horizontally("images", f"page_{page.page_num}_image.png", f"page_{page.page_num}_text_image.png", f"page_{page.page_num}_combined_image.png"):
        # Delete the cover image and the text image
        os.remove(f"images/page_{page.page_num}_image.png")
        os.remove(f"images/page_{page.page_num}_text_image.png")
        print(f"Deleted images/page_{page.page_num}_image.png and images/page_{page.page_num}_text_image.png")
    else:
        print(f"Failed to merge images for page {page.page_num}.")
    print(f"==> Done processing page {page.page_num}")

async def process_page_async(page, all_character_features, resolution, page_font, seed):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, process_page, page, all_character_features, resolution, page_font, seed)

async def get_storybook_illustration(title, characters, cover_picture_description, num_pages, pages):
    import time  # Import the time module

    start_time = time.time()  # Record the start time
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
        features = character.character_features
        all_character_features += f"Name of Character: {character_name}:\n\nFeatures of {character_name}: {features}:\n"

    if usingDallE:
        resolution = "1024x1024"
    else:
        resolution = "800X1280"

    random_number = random.randint(1, 10000000)
    page_font = get_random_font()
    seed = random_number

    # Generate Page Pictures in parallel
    tasks = [
        generate_cover_page_async(cover_picture_description, all_character_features, title, resolution, random_number),
        *[
            process_page_async(page, all_character_features, resolution, page_font, seed)
            for page in pages
        ]
    ]
    await asyncio.gather(*tasks)

    # Generate PDF
    storybook_name = title + ".pdf" # If you want to generate the images else where add filepath to the name here?
    convert_images_to_pdf("images", storybook_name)
    print(f"PDF created successfully: {storybook_name}")

    # Clean up the images folder
    for file in os.listdir("images"):
        os.remove(os.path.join("images", file))
    end_time = time.time()  # Record the end time
    execution_time = end_time - start_time  # Calculate the execution time
    print(f"Execution time for get_storybook_illustration: {execution_time:.2f} seconds")

    return storybook_name
