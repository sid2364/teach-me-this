import os
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader, DirectoryLoader

import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
import glob

from tqdm import tqdm

from langchain_huggingface import HuggingFaceEmbeddings

import lancedb
from langchain_community.vectorstores import LanceDB

HF_TOKEN = "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"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HF_TOKEN

embedding_model_name = 'sentence-transformers/all-MiniLM-L6-v2'
model_name = "sentence-transformers/all-MiniLM-L6-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

pdf_files = glob.glob('data/*.pdf')
print("Loading documents: ", pdf_files)
all_docs = []

for file_path in tqdm(pdf_files, desc="Reading books"):
    # Load each document using PyPDFLoader
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    all_docs.extend(docs)

docs = all_docs

def clean_text(text):
    # Replace multiple newlines or special characters with a space
    cleaned = re.sub(r'\n+', ' ', text)
    # Remove any other special characters (optional)
    cleaned = re.sub(r'[_\n]', ' ', cleaned)
    # Normalize spaces (replace multiple spaces with a single space)
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

db = lancedb.connect("lance_database")
table = db.create_table(
    "rag_tmt",
    data=[
        {
            "vector": embeddings.embed_query("Hello Computer"),
            "text": "Hello computer!",
            "id": "1",
        }
    ],
    mode="overwrite",
)

docsearch = LanceDB.from_documents(all_chunks, embeddings, connection=db)

from langchain.prompts.prompt import PromptTemplate
from langchain.schema.messages import get_buffer_string
from langchain_core.prompts import ChatPromptTemplate

prompt_template = """
You are a helpful AI assistant. Your name is Jarvis

Use the following information fetched from the PDF provided by the user to answer the question:
{context}

Question: {query}
Answer:
"""

prompt = PromptTemplate(
    input_variables=["context", "query"],
    template=prompt_template
)

#my_query = "What is the name of the pony that Sam Gamgee acquires in Bree after Bill Ferny sells them Bill the Pony?"
my_query = "What did Eärendil say to Elwing before he went up alone into the land and came into the Calacirya?"

retriever = docsearch.as_retriever(search_kwargs={"k": 3})
docs = retriever.get_relevant_documents(my_query)
print(docs)
from langchain_community.llms import HuggingFaceHub

# Model architecture
llm_repo_id = "huggingfaceh4/zephyr-7b-alpha"
model_kwargs = {"temperature": 0.5, "max_length": 4096, "max_new_tokens": 2048}
model = HuggingFaceHub(repo_id=llm_repo_id, model_kwargs=model_kwargs)

from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough

# rag_chain = (
#         {"context": retriever,  "query": RunnablePassthrough()}
#         | prompt
#         | model
#         | StrOutputParser()
# )

rag_chain = (
        retriever  # Get relevant documents
        | (lambda docs: {"context": "\n".join([doc.page_content for doc in docs]), "query": my_query})  # Combine context and query
        | prompt  # Format the prompt with the context and query
        | model  # Get the model response
        | StrOutputParser()  # Parse the model response
)

print(retriever)
print(rag_chain)
response = rag_chain.invoke(my_query)
print("-"*20)
print(response)
