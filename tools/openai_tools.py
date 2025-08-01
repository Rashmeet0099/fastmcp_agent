import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with the API key from the environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(text: str) -> str:
    # ... (rest of your function code remains the same)
    if not client.api_key:
        return "Error: OpenAI API key is not set. Please set it in the .env file."
        
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
                {"role": "user", "content": f"Summarize the following text: {text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred while calling the OpenAI API: {e}"