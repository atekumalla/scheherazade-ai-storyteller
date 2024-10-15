from PIL import Image, ImageDraw, ImageFont
import os

"""
This file contains the code for the page text to image generation.
"""

cover_text_font_size = 72
page_text_font_size = 48

font_to_use = [
    "Optima.ttc",
    "Futura.ttc",
    "GillSans.ttc",
    "HelveticaNeue.ttc",
    "MarkerFelt.ttc",
    "Georgia.ttf"
]

import random

def get_random_font():
    """
    Returns a random font from the font_to_use list.
    
    Returns:
    str: A randomly selected font name from the font_to_use list.
    """
    font_name = random.choice(font_to_use)
    font_path = os.path.join(os.path.dirname(__file__), 'fonts', font_name)
    return font_path


def parse_resolution(resolution_string):
    """
    Parse a resolution string in the format 'widthxheight' and return width and height as integers.
    
    Args:
    resolution_string (str): A string in the format 'widthxheight', e.g., '800x1280'
    
    Returns:
    tuple: A tuple containing two integers (width, height)
    
    Raises:
    ValueError: If the input string is not in the correct format
    """
    try:
        width, height = map(int, resolution_string.lower().split('x'))
        return width, height
    except ValueError:
        raise ValueError("Invalid resolution format. Expected 'widthxheight', e.g., '800x1280'")

# Example usage:
# resolution = "800x1280"
# width, height = parse_resolution(resolution)
# print(f"Width: {width}, Height: {height}")

def generate_image_from_page_text(page_text, resolution, filename, folder_name, is_cover=False, font_to_use=None):
    """
    Generate an image from a given page text and resolution.
    
    Args:
    page_text (str): The text describing the image to be generated
    resolution (str): The resolution of the image in the format 'widthxheight', e.g., '800x1280'
    filename (str): The name of the file to save the generated image
    folder_name (str): The name of the folder to save the generated image
    
    Returns:
    str: the filename of the generated image

    """
    width, height = parse_resolution(resolution)
    if font_to_use is None:
        font_to_use = get_random_font()

    # Create a blank image
    # TODO: Add a background image based on the input image/prompt
    image = Image.new('RGB', (width, height), color = 'white')

    # Initialize ImageDraw
    draw = ImageDraw.Draw(image)

    if is_cover:
        font_size = cover_text_font_size
    else:
        font_size = page_text_font_size

    # Define text and font
    text = page_text
    print("Using font:")
    print(font_to_use)
    large_font = ImageFont.truetype(font_to_use, font_size)

    # Split the text into lines and wrap long lines
    lines = []
    for line in text.split('\n'):
        words = line.split()
        current_line = words[0]
        for word in words[1:]:
            test_line = current_line + " " + word
            line_width = draw.textbbox((0, 0), test_line, font=large_font)[2] - draw.textbbox((0, 0), test_line, font=large_font)[0]
            if line_width <= width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)

    # Calculate total height of all lines
    line_heights = [draw.textbbox((0, 0), line, font=large_font)[3] - draw.textbbox((0, 0), line, font=large_font)[1] for line in lines]
    total_height = sum(line_heights)

    # Calculate starting y position to center all lines vertically
    y = (height - total_height) / 2

    # Draw each line centered horizontally
    for i, line in enumerate(lines):
        # Calculate width of this line
        line_width = draw.textbbox((0, 0), line, font=large_font)[2] - draw.textbbox((0, 0), line, font=large_font)[0]
        
        # Calculate x position to center this line horizontally
        x = (width - line_width) / 2
        # Draw the line
        #TODO: Change the color of the text based on the input image/prompt
        draw.text((x, y), line, font=large_font, fill="black")
        # Move y position down for next line
        y += line_heights[i]
    # Save the image
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    image_path = os.path.join(folder_name, filename)
    image.save(image_path)
    
def merge_images_horizontally(images_folder, image1_path, image2_path, output_filename):
    """
    Merge two images horizontally and save the result.
    
    Args:
    images_folder (str): The folder containing the images
    image1_path (str): The path to the first image
    image2_path (str): The path to the second image
    output_filename (str): The name of the file to save the merged image. It will be saved in the images folder.
    """
    # Check if the folder exists
    if not os.path.exists(images_folder):
        print(f"Error: Folder '{images_folder}' does not exist.")
        return False

    # Check if both files exist
    if not os.path.isfile(os.path.join(images_folder, image1_path)):
        print(f"Error: File '{image1_path}' does not exist in '{images_folder}'.")
        return False
    if not os.path.isfile(os.path.join(images_folder, image2_path)):
        print(f"Error: File '{image2_path}' does not exist in '{images_folder}'.")
        return False

    # If all checks pass, open the images
    img1 = Image.open(os.path.join(images_folder, image1_path))
    img2 = Image.open(os.path.join(images_folder, image2_path))

    # Get the heights of the images
    height1 = img1.height
    height2 = img2.height

    # Use the maximum height for the new image
    max_height = max(height1, height2)

    # Create a new image with the width of both images and the max height
    new_img = Image.new('RGB', (img1.width + img2.width, max_height))

    # Paste the first image
    new_img.paste(img1, (0, 0))

    # Paste the second image
    new_img.paste(img2, (img1.width, 0))

    # Save the merged image
    output_path = os.path.join(images_folder, output_filename)
    new_img.save(output_path)

    print(f"Merged image saved as {output_path}")
    return True


# generate_image_from_page_text("The Great Bicycle Race", "800x1280", "cover.png", "images", is_cover=True)
# generate_image_from_page_text("Generate a picture for a children's story book using the following prompt: The cover picture shows Momo and Kiki tugging at a golden banana with Mama Monkey swinging towards them from a nearby tree. The backdrop is a lush green jungle.\n        Below you will find a description of each characters that you may need to use for the cover picture based on the above description.", "800x1280", "output.png", "images", is_cover=False)
# merge_images_horizontally("images","cover.png", "output.png", "merged_image.png")
