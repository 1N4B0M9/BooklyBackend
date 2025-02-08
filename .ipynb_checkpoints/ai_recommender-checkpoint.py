import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API Key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise RuntimeError("OPENAI_API_KEY is not set. Check your .env file or environment variables.")

# Set OpenAI API key
openai.api_key = openai_api_key

def get_recommendations(titles, user_preference):
    prompt = (
        f"The user has the following books on their shelf: {', '.join(titles)}. "
        f"They are looking for a book that matches this preference: '{user_preference}'. "
        f"Select 3 books from their shelf that best match their reading preference. "
        f"Provide the recommendations in a structured format with the title, author, and a short reason why each book was selected."
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    recommendation_text = response["choices"][0]["message"]["content"]
    # Split the recommendations by newline (or comma, depending on format)
    recommendations = [rec.strip() for rec in recommendation_text.split("\n") if rec.strip()]
    return recommendations