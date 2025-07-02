app.py

import streamlit as st 
import requests

st.set_page_config(page_title="Simple Legal AI App") st.title("🧾 Legal Assistant - Simple Version")

--- Memory for conversation ---

if "chat_memory" not in st.session_state: st.session_state.chat_memory = []

--- Module 1: Conversational Document Drafting ---

st.header("1. Document Drafting") draft_input = st.text_input("Describe the legal document you want (e.g., NDA between two parties):")

if draft_input: doc_response = f"Here is a basic draft based on your request:\n\nThis is a {draft_input}. Please review and customize party names, dates, and terms as needed.\n\n---\n\n[Legal Content Placeholder]" st.session_state.chat_memory.append((draft_input, doc_response)) st.markdown("Drafted Document:") st.write(doc_response)

--- Module 2: Legal Clarification ---

st.header("2. Legal Clarification") clarify_input = st.text_input("Ask a legal clarification question (e.g., What is a void contract?):")

def search_duckduckgo(query): url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&no_html=1" r = requests.get(url) data = r.json() return data.get("Abstract", "No direct answer found. Please try a more specific question.")

if clarify_input: clarification = search_duckduckgo(clarify_input) st.markdown("Clarification Result:") st.write(clarification)

--- Chat History (Optional display) ---

st.header("Chat History") for user_q, bot_a in st.session_state.chat_memory: st.markdown(f"You: {user_q}") st.markdown(f"AI: {bot_a}")
