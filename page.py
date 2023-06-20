from st_pages import Page, show_pages
import os

## creating save folders
main_save = "files/"
doc_save = "docs/"
ques_save = "ques/"
output_save = "output/"
os.makedirs("text_data/", exist_ok=True)
os.makedirs(main_save, exist_ok=True)
os.makedirs(main_save+doc_save, exist_ok=True)
os.makedirs(main_save+ques_save, exist_ok=True)
os.makedirs(main_save+output_save, exist_ok=True)

"## Welcome to MyPDF-GPT"
show_pages(
    [
        Page("docs.py", "Documents", ""),
        Page("ques.py", "Question File", ""),
        Page("recollect.py", "Recollect DB", ""),
    ]
)