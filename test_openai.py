import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

try:
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        # model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Tell me a joke"}]
    )
    print("Success ✅", response.choices[0].message['content'])
except Exception as e:
    print("Error ❌", e)
