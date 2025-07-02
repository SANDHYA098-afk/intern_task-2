import streamlit as st
import requests

st.set_page_config(page_title="Legal Chat Assistant", layout="centered")

# ------------------- Session Setup -------------------
if "step" not in st.session_state: st.session_state.step = "start"
if "doc_type" not in st.session_state: st.session_state.doc_type = ""
if "answers" not in st.session_state: st.session_state.answers = {}
if "party_stage" not in st.session_state: st.session_state.party_stage = "a_name"
if "draft" not in st.session_state: st.session_state.draft = ""
if "submitted" not in st.session_state: st.session_state.submitted = False
if "mode" not in st.session_state: st.session_state.mode = "chat"
if "user_input" not in st.session_state: st.session_state.user_input = ""

# ------------------- Document & Law Types -------------------
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

# ------------------- Legal Q&A (DuckDuckGo API) -------------------
def get_legal_answer(question):
    url = f"https://api.duckduckgo.com/?q={question}&format=json"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("Abstract"):
            return f"📘 *Answer:* {data['Abstract']}"
        else:
            return "🤔 I couldn't find a clear definition."
    except Exception as e:
        return f"⚠ Error: {e}"

# ------------------- UI -------------------
st.title("⚖ Legal Chat Assistant")
mode = st.radio("Choose a mode:", ["📝 Draft Legal Document", "🔍 Ask Legal Question"])

# ------------------- Input Box With Auto-Clear -------------------
st.text_input("You:", key="user_input", on_change=lambda: st.session_state.update({'submitted': True}))

# ------------------- MODE 1: Legal Document Drafting -------------------
if mode == "📝 Draft Legal Document" and st.session_state.submitted:
    user_input = st.session_state.user_input.strip()
    st.session_state["user_input"] = ""
    st.session_state["submitted"] = False

    if st.session_state.step == "start":
        st.write("Assistant: What type of legal document do you want to draft?")
        for i, doc in enumerate(doc_types):
            st.write(f"{i + 1}. {doc}")
        st.session_state.step = "doc_type"

    elif st.session_state.step == "doc_type":
        if user_input.isdigit() and 1 <= int(user_input) <= len(doc_types):
            st.session_state.doc_type = doc_types[int(user_input) - 1]
            st.session_state.step = "party_a"
            st.session_state.party_stage = "a_name"
            st.write("Assistant: Enter Party A's full name:")
        else:
            st.error("Please enter a valid number from the list above.")

    elif st.session_state.step == "party_a":
        if st.session_state.party_stage == "a_name":
            st.session_state.answers["a_name"] = user_input
            st.session_state.party_stage = "a_address"
            st.write("Assistant: Enter Party A's address:")
        elif st.session_state.party_stage == "a_address":
            st.session_state.answers["a_address"] = user_input
            st.session_state.party_stage = "a_state"
            st.write("Assistant: Enter Party A's state:")
        elif st.session_state.party_stage == "a_state":
            st.session_state.answers["a_state"] = user_input
            st.session_state.party_stage = "a_contact"
            st.write("Assistant: Enter Party A's contact number:")
        elif st.session_state.party_stage == "a_contact":
            st.session_state.answers["a_contact"] = user_input
            st.session_state.step = "party_b"
            st.session_state.party_stage = "b_name"
            st.write("Assistant: Enter Party B's full name:")

    elif st.session_state.step == "party_b":
        if st.session_state.party_stage == "b_name":
            st.session_state.answers["b_name"] = user_input
            st.session_state.party_stage = "b_address"
            st.write("Assistant: Enter Party B's address:")
        elif st.session_state.party_stage == "b_address":
            st.session_state.answers["b_address"] = user_input
            st.session_state.party_stage = "b_state"
            st.write("Assistant: Enter Party B's state:")
        elif st.session_state.party_stage == "b_state":
            st.session_state.answers["b_state"] = user_input
            st.session_state.party_stage = "b_contact"
            st.write("Assistant: Enter Party B's contact number:")
        elif st.session_state.party_stage == "b_contact":
            st.session_state.answers["b_contact"] = user_input
            st.session_state.step = "jurisdiction"
            st.write("Assistant: Enter the jurisdiction (e.g., Chennai, Delhi):")

    elif st.session_state.step == "jurisdiction":
        st.session_state.answers["jurisdiction"] = user_input
        st.session_state.step = "law"
        st.write("Assistant: Select applicable law by number:")
        for i, law in law_types.items():
            st.write(f"{i + 1}. {law}")

    elif st.session_state.step == "law":
        if user_input.isdigit() and 1 <= int(user_input) <= len(law_types):
            st.session_state.answers["law"] = law_types[int(user_input) - 1]

            a = st.session_state.answers
            doc_type = st.session_state.doc_type.upper()
            draft = f"""
            LEGAL DOCUMENT: {doc_type}

            THIS AGREEMENT is made between:

            PARTY A:
            Name: {a['a_name']}
            Address: {a['a_address']}
            State: {a['a_state']}
            Contact: {a['a_contact']}

            AND

            PARTY B:
            Name: {a['b_name']}
            Address: {a['b_address']}
            State: {a['b_state']}
            Contact: {a['b_contact']}

            Jurisdiction: {a['jurisdiction']}
            Governing Law: {a['law']}

            Both parties agree to abide by the terms and conditions outlined in this document.

            [Disclaimer: This is an AI-generated draft. Please verify with legal counsel.]
            """
            st.session_state.draft = draft.strip()
            st.session_state.step = "completed"
        else:
            st.error("Please enter a valid number from the list above.")

    elif st.session_state.step == "completed":
        st.subheader("📄 Document Preview")
        st.code(st.session_state.draft, language="text")
        st.download_button("⬇ Download Document", st.session_state.draft, file_name="legal_document.txt")

        if st.button("🔄 Start Over"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()

# ------------------- MODE 2: Legal Q&A -------------------
elif mode == "🔍 Ask Legal Question":
    question = st.text_input("Ask your legal question here:")
    if question:
        with st.spinner("Searching..."):
            result = get_legal_answer(question)
            st.markdown(result)
