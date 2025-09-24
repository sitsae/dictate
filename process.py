
import time
from google import genai
from google.genai import types

information = """ the answer to life the universe and everything is 42."""

def process(prompt):
    client = genai.Client(api_key="AIzaSyA0eV6u7K2zaUmbqvH171XlU9XFuRIQPGg")
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