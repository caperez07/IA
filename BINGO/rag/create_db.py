import argparse
import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from embedding_function import get_embedding_function
# from langchain_chroma import Chroma
from langchain_community.vectorstores.chroma import Chroma

DATA_PATH = 'data'
CHROMA_PATH = 'chroma'
MAX_BATCH_SIZE = 5461

def main():
    # checa se o db precisa ser limpo
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("Clearing the database")
        clear_database()

    # cria ou atualiza os documentos
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)

def load_documents():
    print(f"Loading documents from {DATA_PATH}")
    document_loader = PyPDFDirectoryLoader(DATA_PATH) # langchain documentation para diferentes tipos de arquivos
    documents = document_loader.load()
    print(f"Loaded {len(documents)} documents.")
    return documents

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def add_to_chroma(chunks: list[Document]):
    # carregando db
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    # page id
    chunks_with_ids = calculate_chunk_ids(chunks)

    # adicionando ou atualiza os documentos
    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # adiciona apenas os documentos que nao estao no db
    new_chunks = [chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids]
    # new_chunks = []
    # for chunk in chunks_with_ids:
    #     if chunk.metadata["id"] not in existing_ids:
    #         new_chunks.append(chunk)
    
    # if len(new_chunks) != len(chunks_with_ids):
    #     print(f"Error: Length mismatch between chunks and IDs.")
    #     return

    if len(new_chunks):
        print(f"Adding new documents: {len(new_chunks)}")
        new_chunks_ids = [chunk.metadata["id"] for chunk in new_chunks]

        # db.add_documents(new_chunks, ids=new_chunks_ids)

        for i in range(0, len(new_chunks), MAX_BATCH_SIZE):
            batch_chunks = new_chunks[i:i + MAX_BATCH_SIZE]
            batch_ids = new_chunks_ids[i:i + MAX_BATCH_SIZE]
            db.add_documents(batch_chunks, ids=batch_ids)
            print(f"Added batch {i // MAX_BATCH_SIZE + 1} with {len(batch_chunks)} documents")

        db.persist()
        print("Added new documents")
        # db.persist() -> depreciado na nova versao do Chroma
    else:
        print("No new documents to add")
    

def calculate_chunk_ids(chunks):
    # cria os IDs tipo 'data/monopoly.pdf:6:2
    # page source : page number : chunk index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # caso o id da pagina seja igual ao interior, incrementa o index
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # calcula o chunk id
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # adiciona o chunk id ao metadata
        chunk.metadata["id"] = chunk_id
    
    return chunks

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

if __name__ == "__main__":
    main()