# myPDF-GPT
myPDF-GPT is designed to gather information from various sources, including the internet and local data, which can be used to create prompts. OpenAI's GPT-2 model can then utilize these prompts to generate answers that are subsequently stored in a database for future reference.

To accomplish this, the text is first transformed into a fixed-size vector using either open-source or OpenAI models. When a query is submitted, the text is transformed into a vector and compared to the stored knowledge embeddings. The most relevant information is then selected and used to generate a prompt context.

myPDF-GPT supports information sources such as PDFs and documents (Docs). This allows for a diverse range of information to be gathered and used for generating prompts and answers.

### Steps:
Step 1: Use the latest version from the repository: pip install -r requirements.txt

Step 2: How to use

* Set Your API Key
* Go to OpenAI > Account > Api Keys
* Create a new secret key and copy it
* Enter the key to file name documentGPT_V2.py


# Screenshots
## 1. Welcome Page
![Screenshot (39)](https://github.com/apurvprakashshrivastava/myPDF-GPT/assets/69256694/91853e7b-7de4-4c95-8711-25cbb088d503)
## 2. Upload all PDFs
![Screenshot (40)](https://github.com/apurvprakashshrivastava/myPDF-GPT/assets/69256694/e20765c6-b310-4a9c-b98c-83b223a64034)
## 3. Upload the Question .txt file
![Screenshot (41)](https://github.com/apurvprakashshrivastava/myPDF-GPT/assets/69256694/617922aa-5383-4a2b-9c26-b2f1dcc3a94f)
## 4. Uses ChromaDB as Database to restore the lost Files
![Screenshot (42)](https://github.com/apurvprakashshrivastava/myPDF-GPT/assets/69256694/f00378ec-84bd-48f0-8ea9-48de6c0cb376)
