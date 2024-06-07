import requests
import streamlit as st

st.title("Simple Chat Interface")

user_message = st.text_input("Enter your message:")

if user_message:
    data = {"query": user_message}

    response = requests.post("http://app:8080/chat", json=data)

    if response.status_code == 200:
        chat_response = response.json()

        st.write("AI Response:")
        st.write(chat_response["result"])
    else:
        st.error(
            "Failed to get response from the backend. Status code: {}".format(response.status_code)
        )
