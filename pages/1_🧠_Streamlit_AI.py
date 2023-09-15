import streamlit as st
from app.components.chat import display_chat
from app.components.sidebar import sidebar
from app.langchain.chains import qa_chain
import pickle

def initialise():
    if 'knowledge_base' not in st.session_state:
        with open("vectorstore/" + st.secrets["AWS_VECTORSTORE_NAME"], 'rb') as f: 
            vectorstore = pickle.load(f)
        st.session_state['knowledge_base'] = vectorstore

def main():
    st.set_page_config(page_title="Streamlit AI", page_icon="🧠")
    initialise()
    sidebar()
    st.header('🧠 Streamlit AI')
    st.caption("Any Q/A related to Streamlit!")
    with st.expander('⚠️ Disclaimer', expanded=True):
        st.markdown("For prototype we have used only Streamlit github docs for the context of the chatbot.")
        st.markdown("We have used OpenAI API for the embeddings and FAISS for the vector store.")

    if st.session_state['knowledge_base'] is not None:
        display_chat(qa_chain)


if __name__ == "__main__":
    main()