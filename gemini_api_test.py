from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key="AQ.Ab8RN6LjgnqKme9-7DoME7w86zid0iqbaxTb7MTae0vSZ-LbtQ")

response = client.models.generate_content(
    model="gemini-3-flash-preview", contents="AI가 어떻게 동작하는지 한 문장으로 설명해주세요"
)
print(response.text)