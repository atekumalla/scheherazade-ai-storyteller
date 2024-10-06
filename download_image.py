import requests
import os

"""
This script downloads an image from a given URL and saves it to a specified folder.
"""

# Flag to use DallE instead of ideogram
usingDallE = True

def download_file(url, filename, folder_name):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Construct the full file path
    file_path = os.path.join(folder_name, filename)
    if not usingDallE:
        headers = {
            'Authorization': f'Bearer {os.getenv("IDEOGRAM_API_KEY")}',
            'User-Agent': 'YourAppName/1.0',
            'Referer': f'{os.getenv("IDEOGRAM_ENDPOINT")}'
        }
    else: 
        headers = {}
    
    
    print("==> DEBUG: Headers:", headers)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {filename} successfully to {folder_name}.")
    else:
        print("Failed to download the file.")
        print("Error Status Code :", response.status_code)
        print("Error Message: ", response.text)
        
        
# Uagae
download_file("https://oaidalleapiprodscus.blob.core.windows.net/private/org-aunNVr0rseSt5Fvflw7TItdz/user-14tb8jF12nffSjHxWpvcVJ97/img-ly3Bxgvo2Pf8J18gWYcighIj.png?st=2024-10-06T19%3A44%3A53Z&se=2024-10-06T21%3A44%3A53Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-10-06T00%3A40%3A01Z&ske=2024-10-07T00%3A40%3A01Z&sks=b&skv=2024-08-04&sig=zcMCcNnFSWQsrq9nhJ6v822c06Za8lnw%2BIsR4G1mkYU%3D", "desert.png", "images")