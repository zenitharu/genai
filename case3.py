from openai import AzureOpenAI
import streamlit as st

import os

os.environ["OPENAI_API_VERSION"] = "2023-12-01-preview"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://aoai-gpt-channels.openai.azure.com/"
os.environ["AZURE_OPENAI_API_KEY"] = "0e223a79e8584fa1a1cadeabcf5fbeb1"


# client = AzureOpenAI(
#     deployment_name="gstgpt35t"
# )

st.title("GlobalSumi Chat Bot ")

client = AzureOpenAI(
    api_version="2023-12-01-preview",
    azure_endpoint="https://aoai-gpt-channels.openai.azure.com/"
)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gstgpt35t"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        
    st.session_state.messages.append({"role": "assistant", "content": response})