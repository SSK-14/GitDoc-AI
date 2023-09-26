import streamlit as st
from app.components.uploader import load_docs, load_github_docs
from app.components.sidebar import sidebar
from app.utils.load_knowledge import create_vectorstore, unzip_file
import pickle
import os

def initialise():
    if 'vectorstore' not in st.session_state:
        st.session_state['vectorstore'] = None
    if 'document_url' not in st.session_state:
        st.session_state['document_url'] = None

def main():
    st.set_page_config(page_title="Build knowledge", page_icon="🛠️")
    initialise()
    sidebar(is_model=False)
    st.header('🛠️ Build your knowledge base')
    build_form = st.empty()
    if st.session_state['vectorstore'] is None:
        with build_form.form("my_form"):
            st.write("""
             1. Enter the documentation repo url.
             2. If repo is private download repo as zip file and upload.
             """)
            st.caption("Note: If file type is set to Docs only the pdf and md files are used.")
            if st.session_state['vectorstore'] is None:
                col1, col2, col3 = st.columns([4,2,2])
                with col1:
                    document_url = st.text_input(
                    "Enter the documentation repo url",
                    placeholder="Example: https://github.com/streamlit/docs")
                with col2:
                    file_type = st.radio("Include File type",["All", "Docs"],horizontal=True)
                with col3:
                    branch = st.text_input(
                    "Enter the branch",
                    value="master",
                    placeholder="Example: master")
                uploaded_file = load_docs()

                submitted = st.form_submit_button("Create knowledge base")
                if submitted and document_url != "":
                    try:
                        st.session_state['document_url'] = document_url
                        if uploaded_file is not None:
                            unzip_path, branch = unzip_file(uploaded_file)
                        else:
                            unzip_path, branch = load_github_docs(document_url, branch)
                        st.session_state['vectorstore'] = create_vectorstore(unzip_path, file_type, branch)
                    except Exception as e:
                        st.error(e)

        if st.session_state['vectorstore'] is not None:
            build_form.empty()
            with open("vectorstore/uploaded.pkl", 'wb') as f:
                pickle.dump(st.session_state['vectorstore'], f)
            with open("vectorstore/uploaded.pkl", "rb") as file:
                st.download_button(
                    label="Download Knowledge base",
                    data=file,
                    file_name="Knowledge-base.pkl",
                    mime="application/octet-stream"
                )
            st.balloons()
            st.success('Knowledge base created!', icon="✅")
            st.info("Start chatting by uploading it in Docs Chat", icon="ℹ️")
            os.remove("vectorstore/uploaded.pkl")
    else:
        st.success('Knowledge base already created!', icon="✅")
        st.info("Refresh the page to create a new one.", icon="ℹ️")


if __name__ == "__main__":
    main()