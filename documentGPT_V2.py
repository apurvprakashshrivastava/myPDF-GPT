import os
import pandas as pd
from transformers import GPT2TokenizerFast
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
import re, platform, PyPDF2
# from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from difflib import SequenceMatcher
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.prompts import PromptTemplate

os.environ["OPENAI_API_KEY"] = "Paste your OPENAI_KEY"

# ================ initializations ===========

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

embeddings = OpenAIEmbeddings()

# prompt_template = """Given the following extracted parts of a long document and a question, create a final answer. If you don't know the answer, just say that you don't know. Don't try to make up an answer.
# ALWAYS return a "SOURCES" part in your answer.
# Respond with a precise answer in one word and increase words wherever required and give source as well.

# QUESTION: {question}
# =========
# {summaries}
# =========
# FINAL ANSWER:"""

# PROMPT = PromptTemplate(
#     template=prompt_template, input_variables=["summaries", "question"]
# )

prompt_template = """Given the following extracted parts of a long document and a question, give a precise answer. If you don't know the answer, just say that you don't know. Don't try to make up an answer.
Respond with a pin point answer in one word and increase words whenever required.

QUESTION: {question}
=========
{summaries}
=========
FINAL ANSWER:"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["summaries", "question"]
)

persist_directory = "chroma_db"

# ======================= Auxiliary Functions ====================================

def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))

def __str_similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def create_document_embedding(doc_path, doc_metadata, txt_save_loc=None, chunk_size=768, chunk_overlap=64):
    chunk_docs = []

    count = 100//len(doc_metadata)
    counter = 0
    temp_counter = 0

    for index in range(len(doc_path)):
        print("Processing file:", doc_path[index])
        current_platform = platform.system()

        if current_platform == "Windows":
            names = doc_path[index].split("\\")[-1].split(".")
        elif current_platform == "Linux":
            names = doc_path[index].split("/")[-1].split(".")
        
        name = names[0]
        ext = names[1]

        if ext != "txt":
            with open(doc_path[index], 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ''
                for page in pdf_reader.pages:
                    text += page.extract_text()

            with open('{}{}_{}.txt'.format(txt_save_loc,temp_counter, name), 'w', encoding='utf-8') as file:
                file.write(text)

            with open('{}{}_{}.txt'.format(txt_save_loc,temp_counter, name), 'r', encoding='utf-8') as f:
                text = f.read()
            
            ## removing hyperlinks
            text = re.sub(r'http\S+', '', text)

        else:
                with open(doc_path[index], 'r', encoding='utf-8') as f:
                    text = f.read()
        

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
            length_function = count_tokens
        )
        chunks = text_splitter.create_documents([text])

        ## adding meta data
        for i in range(len(chunks)):
            chunks[i].metadata = {"source": f"{doc_metadata[index]}-{name}"}

        ## adding chunks to list
        chunk_docs.extend(chunks)

        ## counter for progress bar
        counter += count
        if counter > 100:
            counter = 100
        yield counter

        temp_counter+=1

    if not os.path.isdir(persist_directory):
        print("Folder Created....")
        docsearch = Chroma.from_documents(chunk_docs, embeddings, persist_directory=persist_directory)
        docsearch.persist()
        del docsearch
    else:
        print("Existing Folder Used....")
        docsearch = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        docsearch.add_documents(documents=chunk_docs, embedding=embeddings)
        docsearch.persist()
        del docsearch



def get_answers_from_documents(doc_metadata, questionnaire_loc, num_ans=4, save_file_name = "output.csv"):
    docsearch = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

    ## reading questionnaire file
    with open(questionnaire_loc, "r") as file:
        questions = [line.strip().strip("?").strip(".").strip() for line in file]
    
    ## creatig empty dataframe
    df = pd.DataFrame(columns=['Question', 'Answer', 'Source'])

    count = 100//len(doc_metadata)
    counter = 0

    for doc_name in doc_metadata:
        for ques in questions:
            temp_ques = ques + " for " + doc_name + "?"
            docs = docsearch.similarity_search(temp_ques,k=num_ans)

            ## new docs
            docs_copy = docs.copy()
            for doc in docs_copy:
                source = doc.metadata["source"].split("-")[0]
                if __str_similar(source.lower(), doc_name.lower()) < 0.7:
                    docs.remove(doc)
            
            # QA chain
            chain = load_qa_with_sources_chain(OpenAI(temperature=1), chain_type="stuff", prompt=PROMPT)
            ans_dict = chain({"input_documents": docs, "question": temp_ques}, return_only_outputs=True)
            print("\n\nQuestion:", temp_ques)
            print("Answer:", ans_dict["output_text"].strip())
            df.loc[len(df.index)] = [temp_ques, ans_dict["output_text"].strip(), doc_name]
        
        ## counter for progress bar
        counter += count
        if counter < 100:
            yield counter
    
    ## saving the file
    df.to_csv(save_file_name, index = False)
    counter = 100
    yield counter

# ============================================================================

# ================= driver code ====================
# doc_path = [r"C:\\Users\\Utkarsh\\Desktop\\Sprih\\work\\Dabur.pdf", r"C:\\Users\\Utkarsh\\Desktop\\Sprih\\work\\Godrej Properties Limited.pdf", r"C:\\Users\\Utkarsh\\Desktop\\Sprih\\work\\Grasim Industries.pdf", r"C:\\Users\\Utkarsh\\Desktop\\Sprih\\work\\HCL Technologies.pdf"]
# doc_metadata = ["Dabur", "Godrej Properties Limited", "Grasim Industries", "HCL Technologies"]

# questionnaire_loc = "questions.txt"

# create_document_embedding(doc_path, doc_metadata, chunk_size=192, chunk_overlap=32)

# get_answers_from_documents(doc_metadata, questionnaire_loc, num_ans=4, save_file_name = "output.csv")


# ===================================================