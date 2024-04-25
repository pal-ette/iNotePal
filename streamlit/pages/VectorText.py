import streamlit as st
from streamlit_chat import message
from sentence_transformers import SentenceTransformer
from supabase_client import supabase_client


@st.cache_data()
def cached_model(model_name):
    return SentenceTransformer(model_name)


if "model" not in st.session_state:
    st.session_state["model"] = cached_model("jhgan/ko-sroberta-multitask")


st.header("Supabase Vector DB 테스트")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

with st.form("form", clear_on_submit=True):
    user_input = st.text_input("당신: ", "")
    submitted = st.form_submit_button("전송")

if submitted and user_input:
    embedding = st.session_state["model"].encode(user_input)

    result = (
        supabase_client()
        .rpc(
            "match_sentences",
            {
                "query_embedding": str(embedding.tolist()),
                "match_threshold": 0.0,
                "match_count": 2,
            },
        )
        .execute()
        .data
    )

    st.session_state.past.append(user_input)
    st.session_state.generated.append(result[0]["content"])

for i in range(len(st.session_state["past"])):
    message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
    if len(st.session_state["generated"]) > i:
        message(st.session_state["generated"][i], key=str(i) + "_bot")
