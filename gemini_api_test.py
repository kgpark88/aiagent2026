# google-genai 패키지 설치
# pip install -q -U google-genai

# 실행 명령어 
# python gemini_api_test.py

from google import genai

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key="AIzaSyD_rzFivOejOAy8yrZN6HIqEUIdPYfBZzo")

response = client.models.generate_content(
    model="gemini-3-flash-preview", contents="AI가 어떻게 동작하는지 한 문장으로 설명해주세요"
)
print(response.text)
