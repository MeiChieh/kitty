import openai
import streamlit as st
import os
import time
from helper import *

RATE_LIMIT_SECONDS = 0.5

initial_state_dict = {
    "temperature": 1.5,
    "top_p": 0.8,
    "presence_penalty": 0.5,
    "max_tokens": 300,
    "valid_api_key": False,
    "openai_model": "gpt-4o-mini",
    "is_first_msg": True,
    "messages": [],
}

set_initial_st_state(st.session_state, initial_state_dict)

st.subheader("🐈 Welcome to KITTY")
st.write("(Key Interview Training & Tactics for You)")
st.write(
    "Ready to ace your next interview? KITTY is here to help you think fast, speak confidently, and land that dream job with purr-fection! 😼"
)

api_key = st.sidebar.text_input(
    "🔑 OpenAI API Key", type="password", disabled=st.session_state["valid_api_key"]
)

st.session_state["temperature"] = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=2.0,
    step=0.1,
    value=st.session_state["temperature"],
    help="Controls the creativity and focus of the model.",
)
st.session_state["top_p"] = st.sidebar.slider(
    "Top-P",
    min_value=0.0,
    max_value=1.0,
    step=0.1,
    value=st.session_state["top_p"],
    help="Controls the randomness of the model's output.",
)
st.session_state["presence_penalty"] = st.sidebar.slider(
    "Presence Penalty",
    min_value=-2.0,
    max_value=2.0,
    step=0.1,
    value=st.session_state["presence_penalty"],
    help="Controls the likelihood of the model to talk about new topics.",
)

st.session_state["max_tokens"] = st.sidebar.slider(
    "Max Tokens",
    min_value=0,
    max_value=1000,
    step=10,
    value=st.session_state["max_tokens"],
    help="Controls the length of the generated text.",
)

st.sidebar.button(
    "Restart Chat",
    on_click=lambda: restart_chat(st.session_state),
    help="Clean the chat history and settings and restart a new chat.",
)

client = openai.Client(api_key=api_key)

if not st.session_state["valid_api_key"]:

    if api_key:
        api_key_is_valid = validate_api_key(client)

        if api_key_is_valid:
            st.session_state["valid_api_key"] = True
            message_placeholder = st.empty()
            message_placeholder.success(
                "API key is valid! We can start with the chat!", icon="✅"
            )
            time.sleep(1)
            st.rerun()  # trigger rerender to disable api key entry field

        else:
            st.session_state["valid_api_key"] = False
            message_placeholder = st.empty()
            message_placeholder.warning(
                "API key is invalid! Please enter a valid API key.", icon="⚠️"
            )
            time.sleep(5)
            message_placeholder.empty()

    else:
        st.warning(
            "Please provide your OpenAI API key **in the side panel** to start the chat.",
            icon="🔑",
        )

# don't render the rest of the app without valid_api_key
if not st.session_state["valid_api_key"]:
    st.stop()

# render first chat from the assistant
if st.session_state.is_first_msg:
    st.session_state.messages = send_first_message(st.session_state.messages)
    st.session_state.is_first_msg = False

# render all chats from the state
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message["avatar"]):
        st.markdown(message["content"])


messages = [
    {"role": "system", "content": system_msg},
    {"role": "user", "content": first_assistant_msg},
]

if prompt := st.chat_input("Let's prepare your interview!"):

    st.session_state.messages.append(
        {"role": "user", "content": prompt, "avatar": "👩🏻‍💻"}
    )
    with st.chat_message("user", avatar="👩🏻‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="😺"):

        messages += [
            {"role": msg["role"], "content": msg["content"]}
            for msg in st.session_state.messages
        ]

        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=messages,
            temperature=st.session_state["temperature"],
            top_p=st.session_state["top_p"],
            presence_penalty=st.session_state["presence_penalty"],
            stream=True,
            max_tokens=st.session_state["max_tokens"],
        )
        time.sleep(RATE_LIMIT_SECONDS)
        response = st.write_stream(stream)

    st.session_state.messages.append(
        {"role": "assistant", "content": response, "avatar": "😺"}
    )
