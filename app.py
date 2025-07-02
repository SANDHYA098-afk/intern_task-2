import streamlit as st
import requests

st.set_page_config(page_title="Legal Assistant", layout="centered")

# ------------------- Session Setup -------------------
if "step" not in st.session_state: st.session_state.step = "start"
if "data" not in st.session_state: st.session_state.data = {}
if "doc_drafted" not in st.session_state: st.session_state.doc_drafted = False

# ------------------- Document & Law Options -------------------
doc_types = [
    "Non-Disclosure Agreement (NDA)",
    "Lease Agreement",
    "Employment Contract",
    "IT Services Agreement",
    "Freelance Work Contract"
]

law_types = [
    "Indian Contract Act, 1872",
    "Information Technology Act, 2000",
    "Rent Control Act, 1948",
    "Transfer of Property Act, 1882",
    "Industrial Disputes Act, 1947",
    "Shops and Establishments Act",
    "Copyright Act, 1957"
]

# ------------------- Mode Switch -------------------
mode = st.radio("Choose Mode:", ["📝 Draft Legal Document", "🔍 Ask Legal Question"])

# ==========================
# MODULE 1: DOCUMENT DRAFTING
# ==========================
if mode == "📝 Draft Legal Document":
    st.title("📝 Draft a Legal Document")

    if st.session_state.step == "start":
        doc = st.selectbox("Select the type of document:", doc_types)
        if st.button("Next"):
            st.session_state.data["doc_type"] = doc
            st.session_state.step = "a_name"

    elif st.session_state.step == "a_name":
        name = st.text_input("Party A - Full Name:")
        if name:
            st.session_state.data["a_name"] = name
            st.session_state.step = "a_address"

    elif st.session_state.step == "a_address":
        address = st.text_input("Party A - Address:")
        if address:
            st.session_state.data["a_address"] = address
            st.session_state.step = "a_state"

    elif st.session_state.step == "a_state":
        state = st.text_input("Party A - State:")
        if state:
            st.session_state.data["a_state"] = state
            st.session_state.step = "a_contact"

    elif st.session_state.step == "a_contact":
        contact = st.text_input("Party A - Contact Number:")
        if contact:
            st.session_state.data["a_contact"] = contact
            st.session_state.step = "b_name"

    elif st.session_state.step == "b_name":
        name = st.text_input("Party B - Full Name:")
        if name:
            st.session_state.data["b_name"] = name
            st.session_state.step = "b_address"

    elif st.session_state.step == "b_address":
        address = st.text_input("Party B - Address:")
        if address:
            st.session_state.data["b_address"] = address
            st.session_state.step = "b_state"

    elif st.session_state.step == "b_state":
        state = st.text_input("Party B - State:")
        if state:
            st.session_state.data["b_state"] = state
            st.session_state.step = "b_contact"

    elif st.session_state.step == "b_contact":
        contact = st.text_input("Party B - Contact Number:")
        if contact:
            st.session_state.data["b_contact"] = contact
            st.session_state.step = "jurisdiction"

    elif st.session_state.step == "jurisdiction":
        jurisdiction = st.text_input("Jurisdiction (e.g., Chennai):")
        if jurisdiction:
            st.session_state.data["jurisdiction"] = jurisdiction
            st.session_state.step = "law"

    elif st.session_state.step == "law":
        law = st.selectbox("Select applicable law:", law_types)
        if st.button("Generate Draft"):
            st.session_state.data["law"] = law
            st.session_state.doc_drafted = True
            st.session_state.step = "done"

    if st.session_state.doc_drafted:
        d = st.session_state.data
        draft = f"""
        LEGAL DOCUMENT: {d['doc_type'].upper()}

        THIS AGREEMENT is made between:

        PARTY A:
        Name: {d['a_name']}
        Address: {d['a_address']}
        State: {d['a_state']}
        Contact: {d['a_contact']}

        AND

        PARTY B:
        Name: {d['b_name']}
        Address: {d['b_address']}
        State: {d['b_state']}
        Contact: {d['b_contact']}

        Jurisdiction: {d['jurisdiction']}
        Governing Law: {d['law']}

        Both parties agree to abide by the terms and conditions outlined in this document.

        [Disclaimer: This is an AI-generated draft. Please review with legal counsel.]
        """
        st.markdown("---")
        st.subheader("📄 Drafted Document")
        st.code(draft.strip(), language="text")

        if st.button("🔄 Start Over"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()

# ==========================
# MODULE 2: LEGAL Q&A
# ==========================
elif mode == "🔍 Ask Legal Question":
    st.title("🔍 Ask a Legal Question")
    question = st.text_input("Ask your legal question:")

    def get_legal_answer(q):
        url = f"https://api.duckduckgo.com/?q={q}&format=json"
        try:
            res = requests.get(url)
            data = res.json()
            if data.get("Abstract"):
                return f"📘 *Answer:* {data['Abstract']}"
            elif data.get("RelatedTopics"):
                return f"🔗 Related: {data['RelatedTopics'][0].get('Text', 'No details found.')}"
            else:
                return "❓ Sorry, no clear answer was found."
        except Exception as e:
            return f"⚠ Error: {e}"

    if question:
        with st.spinner("Searching..."):
            response = get_legal_answer(question)
            st.markdown(response)
