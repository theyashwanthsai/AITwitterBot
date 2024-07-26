from crewai_tools import tool
import requests
import os
from dotenv import load_dotenv
from decouple import config
from PIL import Image
import io

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/mann-e/Mann-E_Dreams"
headers = {"Authorization": f"Bearer {config('HUGGINGFACE_API_TOKEN')}"}

def query(payload):
  response = requests.post(API_URL, headers=headers, json=payload)
  response.raise_for_status()  # Ensure we raise an error for bad responses
  return response.content

@tool("Generate image using prompts")
def path_of_image(prompt: str) -> str:
    """Tool to generate AI images based on a prompt. (Text to image)"""
    try:
        # Generate the image
        # image_bytes = query({"inputs": prompt})
        
        # Open the image
        # image = Image.open(io.BytesIO(image_bytes))
        
        # # Define the path to save the image
        # image_path = os.path.join("generated_images", "1.png")
        image_path = "1.png"
        
        # # Ensure the directory exists
        # os.makedirs(os.path.dirname(image_path), exist_ok=True)
        
        # Save the image
        # image.save(image_path)
        
        return image_path
    except Exception as e:
        return str(e)