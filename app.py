# app.py
import streamlit as st
import requests

st.set_page_config(page_title="Legal AI Assistant")
st.title("📜 Legal Document & Clarification Assistant")

# Initialize state for document drafting
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.doc_type = ""
    st.session_state.date = ""
    st.session_state.state = ""
    st.session_state.party_a_name = ""
    st.session_state.party_a_address = ""
    st.session_state.party_a_contact = ""
    st.session_state.party_b_name = ""
    st.session_state.party_b_address = ""
    st.session_state.party_b_contact = ""
    st.session_state.final_draft = ""

st.header("Legal Clarification")
st.markdown("Ask a legal question to clarify your doubts (e.g., void contract, voidable contract etc.)")

def get_clarification(query):
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&no_html=1"
    try:
        res = requests.get(url, timeout=10)
        data = res.json()
        # Try Abstract first
        answer = data.get("Abstract")
        if answer:
            return answer
        # Try RelatedTopics if Abstract is empty
        related = data.get("RelatedTopics", [])
        if related and "Text" in related[0]:
            return related[0]["Text"]
        return "Sorry, I couldn't find a direct answer. Try rephrasing your question."
    except Exception as e:
        return f"Error: {e}"

query = st.text_input("Type your legal question:")
if query:
    answer = get_clarification(query)
    st.markdown("*Answer:*")
    st.write(answer)

st.header("Legal Document Drafting")
st.markdown("Answer a few simple questions to generate your legal document.")

if st.session_state.step == 0:
    st.session_state.doc_type = st.text_input("What type of document is this? (e.g., NDA, Lease Agreement, etc.):")
    if st.session_state.doc_type:
        st.session_state.step = 1

if st.session_state.step == 1:
    st.session_state.date = st.text_input("Enter the date of agreement (e.g., July 2, 2025):")
    if st.session_state.date:
        st.session_state.step = 2

if st.session_state.step == 2:
    st.session_state.state = st.text_input("Enter the state of jurisdiction (e.g., California):")
    if st.session_state.state:
        st.session_state.step = 3

if st.session_state.step == 3:
    st.session_state.party_a_name = st.text_input("Enter Party A's full name:")
    if st.session_state.party_a_name:
        st.session_state.step = 4

if st.session_state.step == 4:
    st.session_state.party_a_address = st.text_input("Enter Party A's residential address:")
    if st.session_state.party_a_address:
        st.session_state.step = 5

if st.session_state.step == 5:
    st.session_state.party_a_contact = st.text_input("Enter Party A's contact number:")
    if st.session_state.party_a_contact:
        st.session_state.step = 6

if st.session_state.step == 6:
    st.session_state.party_b_name = st.text_input("Enter Party B's full name:")
    if st.session_state.party_b_name:
        st.session_state.step = 7

if st.session_state.step == 7:
    st.session_state.party_b_address = st.text_input("Enter Party B's residential address:")
    if st.session_state.party_b_address:
        st.session_state.step = 8

if st.session_state.step == 8:
    st.session_state.party_b_contact = st.text_input("Enter Party B's contact number:")
    if st.session_state.party_b_contact:
        st.session_state.step = 9

if st.session_state.step == 9:
    doc_type = st.session_state.doc_type.upper()
    doc_type_raw = st.session_state.doc_type.lower()
    date = st.session_state.date.title()
    state = st.session_state.state.title()

    a_name = st.session_state.party_a_name.upper()
    a_addr = st.session_state.party_a_address.title()
    a_contact = st.session_state.party_a_contact

    b_name = st.session_state.party_b_name.upper()
    b_addr = st.session_state.party_b_address.title()
    b_contact = st.session_state.party_b_contact

    st.session_state.final_draft = f"""
{doc_type}

This {doc_type_raw} is made on {date}, governed by the laws of {state}.

BETWEEN:
PARTY A: {a_name}, residing at {a_addr}, Contact: {a_contact},
and
PARTY B: {b_name}, residing at {b_addr}, Contact: {b_contact}.

The parties agree to the terms and conditions outlined in this agreement.

[This document embodies the complete understanding and agreement between the Parties.
Both parties acknowledges full comprehension and acceptance of its terms.]

IN WITNESS WHEREOF, the parties have executed this agreement on the date written above.

____________________        ____________________
{a_name}                    {b_name}
"""
    st.subheader("📄 Drafted Document")
    st.text_area("", st.session_state.final_draft, height=300)
    if st.button("Reset Form"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
