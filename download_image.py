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
    headers = {
        'Authorization': f'Bearer {os.getenv("IDEOGRAM_API_KEY")}',
        'User-Agent': 'YourAppName/1.0',
        'Referer': 'https://www.ideogram.ai/'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {filename} successfully to {folder_name}.")
    else:
        print("Failed to download the file.")
        print(response.status_code)
        
        
# Uagae
# download_file("https://ideogram.ai/api/images/ephemeral/y23tOWlaS3iHGjyvGQeWEA.png?exp=1728280913&sig=9789e5108e78c1550c997b8d3e89747e847554765b661dfb53d1ff64edc8168c", "desert.png", "images")