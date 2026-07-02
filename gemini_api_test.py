from google import genai

# API Key - https://aistudio.google.com/api-keys
client = genai.Client(api_key="AQ.Ab8RN6....cwjeTBpI3Q")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="AI가 어떻게 동작하는지 한 문장으로 설명해주세요"
)
print(response.text)