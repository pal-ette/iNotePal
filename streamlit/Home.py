import streamlit as st
from openai import OpenAI
from firebase_auth import sign_in_with_email_and_password, sign_out
import datetime
from streamlit_calendar import calendar
from models.ryugibo import Ryugibo


def load_model(model_type):
    model = None
    if model_type == "ryugibo":
        model = Ryugibo("dummy-0.0.0")
    return model


selected_model = None
if "last_selected_model" not in st.session_state:
    st.session_state["last_selected_model"] = None

with st.sidebar:
    if "firebase" in st.session_state:

        def logout():
            del st.session_state["messages"]
            sign_out()

        st.button(label="로그아웃", on_click=logout)

        selected_model = st.selectbox(label="감정 분류 모델 선택", options=["ryugibo"])
    else:
        email = st.text_input(label="Email", disabled=("firebase" in st.session_state))
        pw = st.text_input(
            label="Password", type="password", disabled=("firebase" in st.session_state)
        )
        if email and pw:
            st.session_state["firebase"] = sign_in_with_email_and_password(email, pw)
            st.rerun()
    calendar = calendar()
    st.write(calendar)

if st.session_state["last_selected_model"] != selected_model:
    st.session_state["last_selected_model"] = selected_model
    with st.spinner("모델 초기화 중..."):
        st.session_state["inference_model"] = load_model(
            st.session_state["last_selected_model"]
        )
if "firebase" in st.session_state:

    def print_history(messages):
        for role, message in messages:
            with st.chat_message(role):
                st.markdown(message)

    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        st.session_state["openai"] = OpenAI(api_key=st.secrets.openai.OPENAI_API_KEY)
        now = datetime.datetime.now()
        response = st.session_state["openai"].chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"당신은 심리상담사입니다. 오늘은 {now.month}월 {now.day}일 입니다. 오늘 날짜와 함께 오늘 기분이 어땠는지 물어봐줘.",
                }
            ],
        )
        response_msg = response.choices[0].message
        st.session_state["messages"].append((response_msg.role, response_msg.content))

    print_history(st.session_state["messages"])
    input = st.chat_input()
    if input:
        st.session_state["messages"].append(("human", input))
        with st.chat_message("human"):
            st.markdown(input)
            st.write(
                st.session_state["inference_model"].predict(
                    st.session_state["inference_model"].padding(
                        st.session_state["inference_model"].tokenize(
                            [
                                input,
                            ],
                        ),
                    ),
                ),
            )
        with st.spinner(text="대답하는 중.."):
            response = st.session_state["openai"].chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": input}],
            )
        response_msg = response.choices[0].message
        with st.chat_message(response_msg.role):
            st.markdown(response_msg.content)
        st.session_state["messages"].append((response_msg.role, response_msg.content))
else:
    st.write("로그인해주세요.")
