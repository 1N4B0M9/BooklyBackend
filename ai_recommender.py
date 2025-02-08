import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise RuntimeError("OPENAI_API_KEY is missing. Set it in Render Environment Variables.")

openai.api_key = openai_api_key

def get_recommendations(titles, user_preference):
    prompt = (
        f"The user has the following books on their shelf: {', '.join(titles)}. "
        f"They are looking for a book that matches this preference: '{user_preference}'. "
        f"Select 3 books from their shelf that best match their reading preference. "
        f"Provide the recommendations in a structured format with the title, author, and a short reason why each book was selected."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        recommendation_text = response["choices"][0]["message"]["content"]
        recommendations = [rec.strip() for rec in recommendation_text.split("\n") if rec.strip()]
        return recommendations
    
    except openai.error.InvalidRequestError as e:
        print(f" OpenAI Invalid Request Error: {e}")
        return {"error": "Invalid request to OpenAI API"}
    
    except openai.error.AuthenticationError as e:
        print(f"OpenAI Authentication Error: {e}")
        return {"error": "Invalid OpenAI API Key"}

    except openai.error.RateLimitError as e:
        print(f"OpenAI Rate Limit Exceeded: {e}")
        return {"error": "OpenAI rate limit exceeded. Please try again later."}
    
    except openai.error.OpenAIError as e:
        print(f" OpenAI API Error: {e}")
        return {"error": "An error occurred with OpenAI API"}