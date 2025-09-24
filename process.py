
from dotenv import load_dotenv
from google import genai
from google.genai import types
load_dotenv()
import os
api_key = os.environ["GEMINI_API_KEY"]

information = """ the answer to life the universe and everything is 42."""

def process(prompt):
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            system_instruction=f"Use this as the only source of truth: {information}"
        ),
        contents=prompt, 
    )

    print(response.text)
    return response.text