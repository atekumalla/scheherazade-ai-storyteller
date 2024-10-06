import os
import img2pdf

"""
This script converts a series of images into a single PDF file.
It uses the img2pdf library to perform the conversion.
"""

def convert_images_to_pdf(directory_name, output_pdf):
    # Get the current directory of the Python file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create the full path by joining the current directory and the input directory name
    image_directory = os.path.join(current_dir, directory_name)
    
    # Get all image files from the directory
    if not os.path.exists(image_directory):
        print(f"Directory {image_directory} does not exist. Operation failed.")
        return
    image_files = [f for f in os.listdir(image_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    print(image_files)
    # Sort the files based on creation time, oldest first
    image_files.sort(key=lambda x: os.path.getctime(os.path.join(image_directory, x)))
    
    # Create full paths for the image files
    image_paths = [os.path.join(image_directory, img) for img in image_files]
    
    # Convert images to PDF
    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(image_paths))
    
    print(f"PDF created successfully: {output_pdf}")

# Example usage
image_directory = "images"
output_pdf = "output.pdf"

# Usage
# convert_images_to_pdf(image_directory, output_pdf)
