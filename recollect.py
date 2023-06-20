from glob import glob
import streamlit as st
import json, platform
from documentGPT_V2 import create_document_embedding

current_platform = platform.system()
seperator = ""
if current_platform == "Windows":
    seperator = "\\"
elif current_platform == "Linux":
    seperator = "/"


if st.button("Press to refresh DB..."):
    files = glob("text_data" + seperator + "*.txt")
    metadata = []
    file = open("metadata.json", "r")
    data = json.load(file)

    for file in files:
        num = file.split(seperator)[-1].split("_")[0]
        metadata.append(data[num])
    
    my_bar = st.progress(0, text="Progress: 0%")
    for percent_complete in create_document_embedding(files, metadata, chunk_size=192, chunk_overlap=32):
        my_bar.progress(percent_complete, text="Progress: {}%".format(percent_complete))
    
    if percent_complete == 100:
        st.write("**Processing Completed. New Chroma DB created...**")