# app.py
import streamlit as st
import requests

st.set_page_config(page_title="Legal AI Assistant")
st.title("📜 Legal Document Drafting & Clarification Assistant")

# Initialize state for document drafting
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.party_a_name = ""
    st.session_state.party_a_address = ""
    st.session_state.party_a_contact = ""
    st.session_state.party_b_name = ""
    st.session_state.party_b_address = ""
    st.session_state.party_b_contact = ""
    st.session_state.final_draft = ""

st.header("2. Legal Clarification")
st.markdown("Ask a legal question (e.g., What is a void contract?)")

def get_clarification(query):
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&no_html=1"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        return data.get("Abstract", "No exact answer found. Try refining your query.")
    else:
        return "OOPS :( Error Occured. TRY AGAIN"

query = st.text_input("Type your legal question:")
if query:
    answer = get_clarification(query)
    st.markdown("*Answer:*")
    st.write(answer)

st.header("1. Legal Document Drafting")
st.markdown("Answer a few simple questions to generate your legal document.")

if st.session_state.step == 0:
    st.session_state.party_a_name = st.text_input("Enter Party A's full name:")
    if st.session_state.party_a_name:
        st.session_state.step = 1

if st.session_state.step == 1:
    st.session_state.party_a_address = st.text_input("Enter Party A's residential address:")
    if st.session_state.party_a_address:
        st.session_state.step = 2

if st.session_state.step == 2:
    st.session_state.party_a_contact = st.text_input("Enter Party A's contact number:")
    if st.session_state.party_a_contact:
        st.session_state.step = 3

if st.session_state.step == 3:
    st.session_state.party_b_name = st.text_input("Enter Party B's full name:")
    if st.session_state.party_b_name:
        st.session_state.step = 4

if st.session_state.step == 4:
    st.session_state.party_b_address = st.text_input("Enter Party B's residential address:")
    if st.session_state.party_b_address:
        st.session_state.step = 5

if st.session_state.step == 5:
    st.session_state.party_b_contact = st.text_input("Enter Party B's contact number:")
    if st.session_state.party_b_contact:
        st.session_state.step = 6

if st.session_state.step == 6:
    a_name = st.session_state.party_a_name.upper()
    a_addr = st.session_state.party_a_address.title()
    a_contact = st.session_state.party_a_contact

    b_name = st.session_state.party_b_name.upper()
    b_addr = st.session_state.party_b_address.title()
    b_contact = st.session_state.party_b_contact

    st.session_state.final_draft = f"""
LEGAL AGREEMENT

This agreement is entered into between:

PARTY A: {a_name}, residing at {a_addr}, Contact: {a_contact},
and
PARTY B: {b_name}, residing at {b_addr}, Contact: {b_contact}.

The parties agree to the terms and conditions outlined in this agreement.

[Insert specific agreement clauses here.]

IN WITNESS WHEREOF, the parties have executed this agreement on this day.

____________________        ____________________
{a_name}                    {b_name}
"""
    st.subheader("📄 Drafted Document")
    st.text_area("", st.session_state.final_draft, height=300)
    if st.button("Reset Form"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
