import streamlit as st
import os, time
import pandas as pd
from documentGPT_V2 import get_answers_from_documents
import json

filename = ""

## getting metadata
metadata = []
file = open("metadata.json", "r")
data = json.load(file)
for value in data.values():
    metadata.append(value)

st.header("Choose the Question File")
uploaded_file = st.file_uploader("Upload TXT question file", type=["txt"])
if uploaded_file is not None:
    filename = uploaded_file.name
    file_path = os.path.join("files/ques", filename)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    st.write("Saved file:", filename)

if st.button("Get Answers"):
   if not uploaded_file:
       st.write("Please upload a file")
   else:
        my_bar = st.progress(0, text="Progress: 0%")
        filename = filename.split(".")[0]
        output_file = "files/output/"+ filename + ".csv"
        for percent_complete in get_answers_from_documents(metadata, file_path, num_ans=7, save_file_name=output_file):
            my_bar.progress(percent_complete, text="Progress: {}%".format(percent_complete))
            if percent_complete == 100:
                time.sleep(1)
                df = pd.read_csv(output_file)
                st.write(df)
                data_as_csv= df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download Output File",
                    data=data_as_csv,
                    file_name='output.csv',
                    mime='text/csv',
                )

               