import os

from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEndpoint

from utils import create_new_db_or_read_existing, get_books_we_read

load_dotenv()

prompt_template = """
You are a helpful AI assistant. Your name is Jarvis

Use the following information fetched from the PDF files provided by the user to answer the question:
{context}

User's question: {query}
Jarvis' Answer:
"""

# Model architecture
llm_repo_id = "huggingfaceh4/zephyr-7b-alpha"
model_kwargs = {"add_to_git_credential": True}


class AnswerParser(StrOutputParser):
    def parse(self, output):
        if "Jarvis' Answer:" in output:
            return output.split("Jarvis' Answer:")[1].strip()
        return output


class Chatbot:
    def __init__(self, retriever, model, prompt):
        self.retriever = retriever
        self.model = model
        self.prompt = prompt
        self.context = ""

    def ask_question(self, user_query):
        docs = self.retriever.invoke(user_query)
        self.context = "\n".join([doc.page_content for doc in docs])

        rag_chain_model = (
            self.retriever  # get relevant document chunks from the PDFs we read
            | (
                lambda docs: {"context": self.context, "query": user_query}
            )  # Combine context and query
            | self.prompt  # format the prompt with the context and query
            | self.model  # fet the model response
            | StrOutputParser()  # parse the model response and make it 'pretty'?
        )

        response = rag_chain_model.invoke(user_query)
        return response, self.context


def main():
    docsearch = create_new_db_or_read_existing()
    # print("Got LanceDB instance from utils: ", docsearch)

    retriever = docsearch.as_retriever(search_kwargs={"k": 8})
    # my_query = "What is the name of the pony that Sam Gamgee acquires in Bree after Bill Ferny sells them Bill the Pony?"
    my_query = "What did Eärendil say to Elwing before he went up alone into the land and came into the Calacirya?"

    model = HuggingFaceEndpoint(
        repo_id=llm_repo_id,
        temperature=0.5,
        max_new_tokens=2048,
        model_kwargs=model_kwargs,
    )

    prompt = PromptTemplate(
        input_variables=["context", "query"], template=prompt_template
    )

    chatbot = Chatbot(retriever, model, prompt)

    print(
        f"\n\nAsk me anything about the books you asked me to read: {"".join(get_books_we_read())}!\n(type 'exit' to end conversation)"
    )

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            break

        response, fetched_data = chatbot.ask_question(user_input)

        '''
        user_input_know = input("Would you like to know how I know? [y|n] ") # cheeky, maybe remove this later
        if user_input_know.lower() in ["y", "yes"]:
            print(f"Fetched Data:-\n{fetched_data}")
            print(f"\nJarvis: {response}")
        else:
            print(f"\nJarvis: {response}")
        '''
        print(f"\nJarvis: {response}")

        print("-" * 20)



if __name__ == "__main__":
    print("Firing things up... This may take a minute (or three)")
    main()
