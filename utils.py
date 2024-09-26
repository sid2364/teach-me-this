import os
import re
from tqdm import tqdm
import glob

import lancedb

from langchain_community.vectorstores import LanceDB
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader, DirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings

# output file where we'll store the names
output_file = 'saved_file_names.txt'
data_dir = 'data'
files_to_read = glob.glob('data/*.pdf')

lancedb_name = "lance_database"

embedding_model_name = 'sentence-transformers/all-MiniLM-L6-v2'
model_name = "sentence-transformers/all-MiniLM-L6-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}

embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)
#todo try OpenAIEmbeddings() instead of HuggingFaceEmbeddings

def create_new_db_or_read_existing():
    # check if files in data are the ones we read before, if so return that instance (not foolproof!)
    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            saved_file_names = file.readlines()
            saved_file_names = [name.strip() for name in saved_file_names]

        if set(saved_file_names) == set(files_to_read):
            return read_lancedb()

    #else write a new lancedb since we don't have these new books stored and return that instance (will take longer)
    docsearch = write_new_lancedb()
    with open(output_file, 'w') as file:
        for filename in files_to_read:
            file.write(f"{filename}\n")
    return docsearch

def read_lancedb():
    db = lancedb.connect(lancedb_name)
    return LanceDB(connection=db, embedding=embeddings)

def write_new_lancedb():
    all_docs = []
    for file_path in tqdm(files_to_read, desc="Reading books"):
        # Load each document using PyPDFLoader
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        all_docs.extend(docs)

    docs = all_docs

    def clean_text(text):
        cleaned = re.sub(r'\n+', ' ', text)
        cleaned = re.sub(r'[_\n]', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    for doc in docs:
        doc.page_content = clean_text(doc.page_content)

    all_chunks = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)

    for doc in tqdm(docs, desc="Splitting documents"):
        chunks = text_splitter.split_documents([doc])
        all_chunks.extend(chunks)

    for i, chunk in enumerate(all_chunks[100:102]):
        print(f"Chunk {i + 1}:\n{chunk.page_content}\n")

    query = "Tell me the length of the embeddings for this document"
    print(len(embeddings.embed_documents([query])[0]))

    db = lancedb.connect(lancedb_name)

    docsearch = LanceDB.from_documents(all_chunks, embeddings, connection=db)
    return docsearch
