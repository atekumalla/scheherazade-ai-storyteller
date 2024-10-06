import requests
import os

"""
This script downloads an image from a given URL and saves it to a specified folder.
"""
def download_file(url, filename, folder_name):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Construct the full file path
    file_path = os.path.join(folder_name, filename)
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {filename} successfully to {folder_name}.")
    else:
        print("Failed to download the file.")
        print(response.status_code)
        
        
# Uagae
# download_file("https://www.idlebrain.com/movie/photogallery/alavaikuntapuramlo2/images/alavaikuntapuramulo2.jpg", "desert.png", "images")