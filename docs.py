import streamlit as st
import os
from documentGPT_V2 import create_document_embedding
import json

doc_path = []
st.header("Choose the PDF File")
uploaded_files = st.file_uploader("Upload PDF File", accept_multiple_files=True, type=["pdf"])

if uploaded_files:
    for uploaded_file in uploaded_files:
        filename = uploaded_file.name
        file_path = os.path.join("files/docs", filename)
        doc_path.append(file_path)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        st.write("Saved file:", filename)

text = st.text_area("Enter metadata (use coma seperated)")
metadata = [meta.strip() for meta in text.split(",")]

if st.button("Vectorize"):
    if not uploaded_files:
        st.write("Please upload a file")
    else:
        my_bar = st.progress(0, text="Progress: 0%")
        for percent_complete in create_document_embedding(doc_path, metadata, txt_save_loc="text_data/", chunk_size=192, chunk_overlap=32):
            my_bar.progress(percent_complete, text="Progress: {}%".format(percent_complete))

        if percent_complete == 100:   
            ## saving metadata as JSON file
            json_data = {i: metadata[i] for i in range(0, len(metadata))}
            with open("metadata.json", "w") as outfile:
                json.dump(json_data, outfile)
            
            st.write("**Processing Completed....**")