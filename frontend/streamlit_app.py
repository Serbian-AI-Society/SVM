import requests
import streamlit as st

# Data
QUERY_SUGGESTIONS = ["Jeo bih nesto kul", 
                     "Nesto bezglutensko",
                     "Jako mi se jede kuvano"]
WARNING_MESSAGE = """
Pazi da se ne prejedes!"""
AUTHORS = """"""
AUTHORS="""
- [Emanuilo Jovanović](https://www.linkedin.com/in/emanuilo-jovanovic-112b7713a/)
- [Marko Nikić](https://www.linkedin.com/in/marko-nikic-471374229/)
- [Milan Lazarević](https://www.linkedin.com/in/mrlaki5/)
"""

# Heading of the page
st.set_page_config(page_title="Klopa?", page_icon="static/icon.ico")
st.title("Gde na klopu?")
st.write("Pitaj me za preporuku restorana 🍔")
st.divider()

# Initialize session state for the selected suggestion
if 'selected_suggestion' not in st.session_state:
    st.session_state.selected_suggestion = ""

# Sidebar
st.logo("static/icon.ico", icon_image="static/icon.ico")
with st.sidebar:
    st.subheader("💡 Sugestije")
    with st.container(border=True, height=200):
        # st.markdown(QUERY_SUGGESTIONS)
        for suggestion in QUERY_SUGGESTIONS:
            if st.button(suggestion):
                st.session_state.selected_suggestion = suggestion

    # st.subheader("⚠️ Upozorenja")
    # with st.container(border=True):
    #     st.markdown(WARNING_MESSAGE)

    st.subheader("✍️ Authors")
    st.markdown(AUTHORS)

    st.markdown("---")  # Adds a horizontal line for separation
    st.markdown("[👨🏻‍💻 Pogledaj izvorni kod](https://github.com/Serbian-AI-Society/SVM)")

user_message = st.text_input("Unesite prohtev", value=st.session_state.selected_suggestion)

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
