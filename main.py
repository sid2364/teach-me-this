import os
from utils import create_new_db_or_read_existing
from langchain.prompts.prompt import PromptTemplate
from langchain_community.llms import HuggingFaceHub
from langchain_core.output_parsers import StrOutputParser


HF_TOKEN = "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"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HF_TOKEN

docsearch = create_new_db_or_read_existing()
print("Got lancedb instance from utils: ", docsearch)

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

retriever = docsearch.as_retriever(search_kwargs={"k": 5})
docs = retriever.get_relevant_documents(my_query)

# Model architecture
llm_repo_id = "huggingfaceh4/zephyr-7b-alpha"
model_kwargs = {"temperature": 0.5, "max_length": 4096, "max_new_tokens": 2048}
model = HuggingFaceHub(repo_id=llm_repo_id, model_kwargs=model_kwargs)

rag_chain = (
        retriever  # get relevant document chunks from the PDFs we read
        | (lambda docs: {"context": "\n".join([doc.page_content for doc in docs]), "query": my_query})  # Combine context and query
        | prompt  # format the prompt with the context and query
        | model  # fet the model response
        | StrOutputParser()  # parse the model response and make it 'pretty'?
)

print(retriever)
print(rag_chain)
response = rag_chain.invoke(my_query)
print("-"*20)
print(response)
