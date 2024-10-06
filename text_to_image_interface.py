# this is a placeholder function that will be implemented later
import requests
from dotenv import load_dotenv
import os
from download_image import download_file
from create_pdf import convert_images_to_pdf

load_dotenv()


def generate_image(image_description, character_features, seed=None):

    PICTURE_PROMPT = f"""Generate a picture for a children's story book using the following prompt: {image_description}
        Below you will find a description of each characters that you may need to use for the cover picture based on the above description.
        {character_features}

        IMPORTANT: Do not have any text describing the story or the title of the story on the images!
    """
    print("\n--->DEBUG: ", PICTURE_PROMPT)
    print("\n--->INPUT SEED: ", seed)

    generation_endpoint = os.getenv("IDEOGRAM_ENDPOINT") + "/generate"
    print("\n--->DEBUG: Generation endpoint:   ", generation_endpoint)
    headers = {
        "Api-Key": f"{os.getenv("IDEOGRAM_API_KEY")}",
        "Content-Type": "application/json"
    }
    if seed is not None:
        payload = { 
            "image_request": {
                "prompt": f"{PICTURE_PROMPT}",
                "aspect_ratio": "ASPECT_10_16",
                "model": "V_2",
                "magic_prompt_option": "AUTO",
                "seed": seed
            } 
        }
    else:
        payload = { 
            "image_request": {
                "prompt": f"{PICTURE_PROMPT}",
                "aspect_ratio": "ASPECT_10_16",
                "model": "V_2",
                "magic_prompt_option": "AUTO"
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

def download_image_from_response(response, filename):
    response_json = response.json()
    image_url = get_image_url(response_json)
    if image_url:
        print(f"---> DEBUG: Image URL: {image_url}")
        download_file(image_url, filename, "images")
    else:
        print("Image URL not found in the response.")

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
        all_character_features += f"Name of Character: {character_name}:\nTraits of {character_name}: {traits}:\nFeatures of {features}:\n"

    #Generating Cover Picture
    response = generate_image(cover_picture_description, all_character_features)
    print(f"--->DEBUG: {response.json()}")
    download_image_from_response(response, "page_0_image.png")
    seed = get_image_seed(response.json())
    print(f"--->DEBUG: Using Seed: {seed} from the cover image")
    # Generate Page Pictures
    for page in pages:
        response = generate_image(page.page_picture_description, all_character_features, seed)
        print(f"--->DEBUG: {response.json()}")
        download_image_from_response(response, f"page_{page.page_num}_image.png")

    # Generate PDF
    storybook_name = title + ".pdf"
    convert_images_to_pdf("images",storybook_name)
    print(f"PDF created successfully: {storybook_name}")

    # Clean up the images folder
    for file in os.listdir("images"):
        os.remove(os.path.join("images", file))

    return response.json()
