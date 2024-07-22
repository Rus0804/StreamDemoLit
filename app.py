import streamlit as st
import os
from llama_index.llms.together import TogetherLLM
from llama_index.embeddings.together import TogetherEmbedding
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
import tempfile
import shutil

# Set API key from environment variable
together_api_key = st.secrets["general"]["together_api_key"]

# Configure the embedding model
Settings.embed_model = TogetherEmbedding(
    model_name="togethercomputer/m2-bert-80M-8k-retrieval",
    api_key=together_api_key
)

# Configure the LLM model
model = 'mistralai/Mixtral-8x7B-Instruct-v0.1'

Settings.llm = TogetherLLM(
    model,
    temperature=0.3,
    max_tokens=512,
    top_p=0.7,
    top_k=50,
    is_chat_model=False,
)

# Title of the app
st.title("File Upload and Query Example")

# Create a temporary directory for uploaded files
if 'temp_dir' not in st.session_state:
    st.session_state.temp_dir = tempfile.mkdtemp()

# File uploader widget for multiple files
uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)

if uploaded_files:
    # Save each uploaded file to the temporary directory
    for uploaded_file in uploaded_files:
        temp_file_path = os.path.join(st.session_state.temp_dir, uploaded_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    
    # Display the list of files
    st.write("Files saved to temporary directory:")
    for file_name in os.listdir(st.session_state.temp_dir):
        st.write(file_name)
        
        # Create a download button for each file
        with open(os.path.join(st.session_state.temp_dir, file_name), "rb") as f:
            st.download_button(
                label=f"Download {file_name}",
                data=f,
                file_name=file_name,
                mime="application/octet-stream"
            )

    # Load documents and create an index
    documents = SimpleDirectoryReader(st.session_state.temp_dir).load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()

    # Query input
    query = st.text_input("Enter your query:")
    if query:
        response = query_engine.query(query)
        st.write("Response:")
        st.write(response)

# Reset button
if st.button("Reset"):
    # Remove the temporary directory and its contents
    if st.session_state.temp_dir and os.path.exists(st.session_state.temp_dir):
        shutil.rmtree(st.session_state.temp_dir)
    # Recreate the temporary directory
    st.session_state.temp_dir = tempfile.mkdtemp()
    # Rerun the script to reset the page
    st.experimental_rerun()
