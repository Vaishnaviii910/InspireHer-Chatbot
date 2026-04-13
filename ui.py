
import streamlit as st
import requests

st.set_page_config(page_title="InspireHer Chatbot", page_icon="🤖")

st.title("🧕 InspireHer Chatbot")
st.markdown("Helping rural women with entrepreneurship, schemes & financial guidance 🇮🇳")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Suggested questions to guide the user
suggested_questions = [
    "What government schemes are available for women entrepreneurs?",
    "How can I start a tailoring business?",
    "What is financial literacy, and why is it important for women?",
    "What online tools can help me manage my business better?",
    "How do I apply for government services online?",
    "What are the eligibility criteria for the PMEGP scheme?",
    "How do I get a loan for my business?",
    "Tell me about Skill Development Scheme for rural women.",
    "What are my rights as a woman entrepreneur?"
]

# Show the list of suggested questions
st.sidebar.title("Suggested Questions")
for question in suggested_questions:
    if st.sidebar.button(question):
        st.session_state.query = question  # Auto-populate the query input
        st.rerun()  # Rerun the app to reflect changes

# Input field for user query
query = st.text_input("💬 Ask your question", value=getattr(st.session_state, 'query', ""))

# Send button logic
if st.button("Send"):
    if query.strip() == "":
        st.warning("Please enter a question.")
    else:
        payload = {
            "query": query,
            "chat_history": st.session_state.chat_history,
        }

        try:
            # response = requests.post("http://localhost:5000/", json=payload)
            response = requests.post("http://0.0.0.0:5000/", json=payload)
            reply = response.json()["response"]

            st.session_state.chat_history.append({"role": "user", "content": query})
            st.session_state.chat_history.append({"role": "assistant", "content": reply})

        except Exception as e:
            st.error(f"Error talking to chatbot: {e}")

# Show conversation history
st.markdown("---")
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"👩‍💼 **You**: {message['content']}")
    else:
        st.markdown(f"🤖 **InspireHer**: {message['content']}")