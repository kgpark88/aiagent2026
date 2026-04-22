# 실행 명령어 
# streamlit run st_summerize_app.py

from google import genai
import streamlit as st


##### Gemini API 요청 함수 #####
def llm_request(prompt, apikey):
    client = genai.Client(api_key=apikey)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text


##### Streamlit UI #####
def main():
    st.set_page_config(page_title="요약 프로그램")
    if "GEMINI_API_KEY" not in st.session_state:
        st.session_state["GEMINI_API_KEY"] = ""

    with st.sidebar:
        api_key = st.text_input(
            label="GEMINI API KEY",
            placeholder="GEMINI API KEY를 입력하세요.",
            value="",
            type="password",
        )
        if api_key:
            st.session_state["GEMINI_API_KEY"] = api_key
        st.markdown("---")

    st.header("📃 문서 요약 서비스")
    st.markdown("---")

    document = st.text_area("요약 할 내용을 입력하세요")
    if st.button("요약하기"):
        prompt = f"""
            [Instructions]
            당신은 [Document]를 한국어로 요약하는 전문가 어시스턴트입니다.
            [[Document]를 읽고, 한국어로 요약하되, 중복된 내용은 생략하고, 중복된 내용을 강조하여 요약하세요.
            요약 시, 사례 증거보다는 개념과 주장을 강조해 주세요.
            요약은 3줄로 간결하게 작성해 주세요.
            요약은 글머리 기호 형태로 제공하세요.
            [Document]
            {document}
            """

        st.info(llm_request(prompt, st.session_state["GEMINI_API_KEY"]))


if __name__ == "__main__":
    main()
