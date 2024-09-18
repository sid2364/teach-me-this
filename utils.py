from tqdm import tqdm
import glob
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader, DirectoryLoader


# Output file where you'll store the names
output_file = 'saved_file_names.txt'
data_dir = 'data'
files_to_read = glob.glob('data/*.pdf')

def create_new_db_or_read_existing():
    # List files and write their names to a file
    with open(output_file, 'r') as file:
        saves_file_names = file.readlines()
        saved_file_names = [name.strip() for name in file_names]

    if set(saved_file_names) == set(files_to_read):
        return read_lancedb()

    #else write a new lancedb since we don't have these new books stored and return that instance (will take longer)

    with open(output_file, 'w') as file:
        for filename in files_to_read:
            file.write(f"{filename}\n")
    return write_new_lancedb()

def read_lancedb():
    pass #todo

def write_new_lancedb():
    for file_path in tqdm(files_to_read, desc="Reading books"):
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


'''
todo
write these functions and make the main.py usethem instead'''