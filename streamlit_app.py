import streamlit as st

import json
from openai import OpenAI

from st_chat_message import message

st.title("Lucas's Historical Figure Chatbot")
st.write(
    "Ask the chatbot who to roleplay as!"
)

client = OpenAI(
    api_key = st.secrets["OPENAI_API_KEY"]
)

system_prompt = """
Assume you are a chatbot roleplaying as a specific historical figure that the user enters in. Your job is to be that historical figure, and answer questions based on what the user asks about that histroical figure.


Always ask the user firsthand on which historical figure they want you to roleplay as.
Be sure to give human responses, and not respond like you are a robot.

"""

if 'convo' not in st.session_state:
    st.session_state["convo"] = [
        {"role": "system", "content": system_prompt}
    ]

    api_call = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages = st.session_state["convo"]
    )
    bot_message = api_call.choices[0].message.content
    st.session_state["convo"].append({"role": "assistant", "content": bot_message})

for chat_message in st.session_state["convo"]:
    if chat_message["role"] == "system":
        continue
    elif chat_message["role"] == "user":
        message(chat_message["content"], is_user=True)
    else:
        message(chat_message["content"])


with st.form("input"):
    user_action = st.text_input("Enter your response here...")
    submitted = st.form_submit_button("Submit")
    if submitted and user_action:
        st.session_state["convo"].append({"role": "user", "content": user_action})
    
        api_call = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages = st.session_state["convo"]
        )


        bot_message = api_call.choices[0].message.content
        st.session_state["convo"].append({"role": "assistant", "content": bot_message})

        st.rerun()
