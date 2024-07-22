import streamlit as st
import tempfile
import os
import shutil

# Title of the app
st.title("File Upload and Download Example with Tempfolder")

# Initialize session state
if 'temp_dir' not in st.session_state:
    st.session_state.temp_dir = None

# Create a temporary directory
if st.session_state.temp_dir is None:
    st.session_state.temp_dir = tempfile.mkdtemp()

# File uploader widget
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

# Reset button
if st.button("Reset"):
    # Remove the temporary directory and its contents
    if st.session_state.temp_dir and os.path.exists(st.session_state.temp_dir):
        shutil.rmtree(st.session_state.temp_dir)
    # Recreate the temporary directory
    st.session_state.temp_dir = tempfile.mkdtemp()
    # Rerun the script to reset the page
    st.experimental_rerun()
