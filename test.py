# save as check_models.py in your backend folder
from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyCRQCSclCzFk7vazarOhlDLEvDKlPop7W8",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

models = [
    "gemini-2.5-flash",
    "gemini-2.0-flash-thinking-exp",
    "gemini-1.5-flash-8b",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro-latest",
    "gemini-exp-1206",
    "learnlm-1.5-pro-experimental"
]

for m in models:
    try:
        r = client.chat.completions.create(
            model=m,
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=10
        )
        print(f"WORKS: {m} -> {r.choices[0].message.content}")
    except Exception as e:
        print(f"FAIL:  {m} -> {str(e)[:100]}")