import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets.openai.OPENAI_API_KEY)


def print_history(messages):
    for role, message in messages:
        with st.chat_message(role):
            st.markdown(message)


if "messages" not in st.session_state:
    st.session_state["messages"] = []

print_history(st.session_state["messages"])
input = st.chat_input()
if input:
    st.session_state["messages"].append(("human", input))
    with st.chat_message("human"):
        st.markdown(input)
    with st.spinner(text="대답하는 중.."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": input}],
        )
    response_msg = response.choices[0].message
    with st.chat_message(response_msg.role):
        st.markdown(response_msg.content)
