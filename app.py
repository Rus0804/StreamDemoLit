import streamlit as st
import tempfile
import os

# Title of the app
st.title("File Upload and Download Example with Tempfile")

# File uploader widget
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        # Write the uploaded file content to the temporary file
        tmp_file.write(uploaded_file.getbuffer())
        tmp_file_path = tmp_file.name
    
    # Display the temporary file path
    st.write("Temporary file saved at:", tmp_file_path)
    
    # Create a download button for the uploaded file
    with open(tmp_file_path, "rb") as f:
        st.download_button(
            label="Download File",
            data=f,
            file_name=uploaded_file.name,
            mime=uploaded_file.type
        )

    # Optionally, you can delete the temporary file if no longer needed
    os.remove(tmp_file_path)

# To run this app, save this code in a file named app.py and run `streamlit run app.py` in your terminal.
