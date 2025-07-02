app.py

import streamlit as st from langchain.chains 
import ConversationChain from langchain.memory 
import ConversationBufferMemory from langchain.chat_models 
import ChatOpenAI from langchain.prompts 
import PromptTemplate 
import requests from PyPDF2 
import PdfReader 
import tempfile 
import os from langchain.vectorstores 
import FAISS from langchain.embeddings 
import HuggingFaceEmbeddings from langchain.text_splitter 
import RecursiveCharacterTextSplitter from langchain.chains.question_answering 
import load_qa_chain

=== Setup ===

st.set_page_config(page_title="Legal AI Suite") st.title("🔖 Legal Conversational Agentic AI Suite")

Memory and LLM setup

llm = ChatOpenAI(temperature=0.5) memory = ConversationBufferMemory() conversation = ConversationChain(llm=llm, memory=memory)

=== Module 1: Conversational Legal Document Drafting ===

st.header("1. Document Drafting") if "doc_memory" not in st.session_state: st.session_state.doc_memory = []

user_input_draft = st.text_input("Describe the legal document you want to draft:") if user_input_draft: response = conversation.run(user_input_draft) st.session_state.doc_memory.append((user_input_draft, response)) st.markdown("Draft Output:") st.write(response)

=== Module 2: External Legal Clarification via DuckDuckGo ===

def search_duckduckgo(query): url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&no_html=1" r = requests.get(url) data = r.json() return data.get("Abstract", "No information found. Please refine your query.")

st.header("2. Legal Clarification") user_query = st.text_input("Ask a legal clarification question:") if user_query: result = search_duckduckgo(user_query) st.markdown("Answer from DuckDuckGo:") st.write(result)

=== Module 3: Document QA via Vector Search ===

st.header("3. Document QA")

if "vectordb" not in st.session_state: st.session_state.vectordb = None

uploaded_file = st.file_uploader("Upload a legal document", type=["pdf", "txt", "docx"])

if uploaded_file: if uploaded_file.type == "application/pdf": reader = PdfReader(uploaded_file) text = "".join([page.extract_text() for page in reader.pages]) else: text = uploaded_file.read().decode("utf-8")

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_text(text)
embed = HuggingFaceEmbeddings()
db = FAISS.from_texts(chunks, embed)
st.session_state.vectordb = db
st.success("Document uploaded and processed.")

query_doc = st.text_input("Ask a question based on the uploaded document:") if query_doc and st.session_state.vectordb: retriever = st.session_state.vectordb.as_retriever() docs = retriever.get_relevant_documents(query_doc) qa_chain = load_qa_chain(llm=llm, chain_type="stuff") answer = qa_chain.run(input_documents=docs, question=query_doc) st.markdown("Answer from Document:") st.write(answer)
