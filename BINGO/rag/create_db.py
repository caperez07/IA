from langchain_community.document_loaders import DirectoryLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.schema import Document
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import Chroma
# import openai 
# from dotenv import load_dotenv
# import os
# import shutil

# import nltk
# # nltk.download('punkt')
# nltk.data.path.append('/path/to/nltk_data')

# DATA_PATH = "data"
# CHROMA_PATH = "chroma"

# def main():
#     generate_data_store()

# def generate_data_store():
#     documents = load_documents()
#     chunks = split_text(documents)
#     save_to_chroma(chunks)

# # carregando a 'base de dados'
# def load_documents():
#     loader = DirectoryLoader(DATA_PATH, glob="*.md")
#     documents = loader.load()
#     return documents

# # separa em chunks cada documento pra n ficar muito grande
# def split_text(documents: list[Document]):
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=500,
#         length_function=len,
#         add_start_index=True,
#     )
#     chunks = text_splitter.split_documents(documents)
#     print(f"Split {len(documents)} documents into {len(chunks)} chunks")

#     document = chunks[0] # aleatorio, so para saber como fica
#     print(document.page_content)
#     print(document.metadata)

#     return chunks

# # salva os chunks em um db
# def save_to_chroma(chunks: list[Document]):
#     # limpa o db (se existir) antes
#     if os.path.exists(CHROMA_PATH):
#         shutil.rmtree(CHROMA_PATH)

#     # Vector Embenddings: é uma representação numérica de um texto
#     # cria o db
#     db = Chroma.from_documents(
#         chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
#     )
#     db.persist()
#     print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}")

# if __name__ == "__main__":
#     main()





import dotenv
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

import nltk
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

REVIEWS_CSV_PATH = "data"
REVIEWS_CHROMA_PATH = "chroma_data"

dotenv.load_dotenv()

loader = DirectoryLoader(REVIEWS_CSV_PATH, glob="*.md")
reviews = loader.load()

reviews_vector_db = Chroma.from_documents(
    reviews, OpenAIEmbeddings(), persist_directory=REVIEWS_CHROMA_PATH
)