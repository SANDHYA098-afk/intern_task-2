import streamlit as st
import requests

st.set_page_config(page_title="Legal Chat Assistant", layout="centered")

# --------------- Session State Setup ---------------
if "step" not in st.session_state: st.session_state.step = "start"
if "doc_type" not in st.session_state: st.session_state.doc_type = ""
if "law_type" not in st.session_state: st.session_state.law_type = ""
if "answers" not in st.session_state: st.session_state.answers = {}
if "draft" not in st.session_state: st.session_state.draft = ""
if "mode" not in st.session_state: st.session_state.mode = "chat"

# --------------- Document and Law Types ---------------
doc_types = [
    "Non-Disclosure Agreement (NDA)",
    "Lease Agreement",
    "Employment Contract",
    "IT Services Agreement",
    "Freelance Work Contract"
]

law_types = {
    0: "Indian Contract Act, 1872",
    1: "Information Technology Act, 2000",
    2: "Rent Control Act, 1948",
    3: "Transfer of Property Act, 1882",
    4: "Industrial Disputes Act, 1947",
    5: "Shops and Establishments Act",
    6: "Copyright Act, 1957"
}

# --------------- DuckDuckGo Legal Q&A Function (Module 2) ---------------
def get_legal_answer(question):
    url = f"https://api.duckduckgo.com/?q={question}&format=json"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("Abstract"):
            return f"📘 *Answer:* {data['Abstract']}"
        else:
            return "🤔 I couldn't find a clear definition. Try using the keyword [Eg. "void contract"]"
    except Exception as e:
        return f"⚠ Error: {e}"

# --------------- App Header and Mode ---------------
st.title("⚖ Legal Chat Assistant")
mode = st.radio("Choose a mode:", ["📝 Draft Legal Document", "🔍 Ask Legal Question"])

# ===================================================
# 📝 MODE 1: Legal Document Drafting
# ===================================================
if mode == "📝 Draft Legal Document":
    user_input = st.text_input("You:")

    if user_input:
        user_input = user_input.strip().lower()

        if st.session_state.step == "start":
            st.write("Assistant: What type of legal document do you want to draft?")
            for i, doc in enumerate(doc_types):
                st.write(f"{i + 1}. {doc}")
            st.session_state.step = "doc_type"

        elif st.session_state.step == "doc_type":
            if user_input.isdigit() and 1 <= int(user_input) <= len(doc_types):
                st.session_state.doc_type = doc_types[int(user_input) - 1]
                st.session_state.step = "party_a"
                st.write("Assistant: Enter Party A's details (format):\n\n*Full Name\nAddress\nState\nContact Number*")
            else:
                st.error("Please enter a number from the list above.")

        elif st.session_state.step == "party_a":
            lines = user_input.split('\n')
            if len(lines) >= 4:
                st.session_state.answers["party_a"] = user_input.strip()
                st.session_state.step = "party_b"
                st.write("Assistant: Enter Party B's details (same format):")
            else:
                st.error("Please enter at least 4 lines.")

        elif st.session_state.step == "party_b":
            lines = user_input.split('\n')
            if len(lines) >= 4:
                st.session_state.answers["party_b"] = user_input.strip()
                st.session_state.step = "jurisdiction"
                st.write("Assistant: Enter the jurisdiction for this agreement (e.g., Chennai, Delhi, Mumbai):")
            else:
                st.error("Please enter at least 4 lines.")

        elif st.session_state.step == "jurisdiction":
            st.session_state.answers["jurisdiction"] = user_input.strip()
            st.session_state.step = "law"
            st.write("Assistant: Select the applicable law by number:")
            for i, law in law_types.items():
                st.write(f"{i + 1}. {law}")

        elif st.session_state.step == "law":
            if user_input.isdigit() and 1 <= int(user_input) <= len(law_types):
                st.session_state.answers["law"] = law_types[int(user_input) - 1]
                st.session_state.step = "generate"
                st.write("Assistant: Generating your document...")
            else:
                st.error("Please enter a valid number from the list.")

        elif st.session_state.step == "generate":
            a = st.session_state.answers
            doc_type = st.session_state.doc_type.upper()
            draft = f"""
            LEGAL DOCUMENT: {doc_type}

            THIS AGREEMENT is made between:

            PARTY A:
            {a['party_a']}

            AND

            PARTY B:
            {a['party_b']}

            Jurisdiction: {a['jurisdiction']}
            Governing Law: {a['law']}

            Both parties agree to abide by the terms and conditions outlined in this document.

            [Disclaimer: This is an AI-generated draft. Please verify with legal counsel.]
            """
            st.session_state.draft = draft.strip()
            st.session_state.step = "completed"

        elif st.session_state.step == "completed":
            st.subheader("📄 Document Preview")
            st.code(st.session_state.draft, language="text")
            st.download_button("⬇ Download Document", st.session_state.draft, file_name="legal_document.txt")

            if st.button("🔄 Start Over"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.experimental_rerun()

# ===================================================
# 🔍 MODE 2: Legal Clarification (DuckDuckGo API)
# ===================================================
elif mode == "🔍 Ask Legal Question":
    question = st.text_input("Ask your legal question here:")
    if question:
        with st.spinner("Searching..."):
            result = get_legal_answer(question)
            st.markdown(result)
