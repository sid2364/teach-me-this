# teach-me-this

Use a Retrieval Augmented Generation (RAG) system alongside an open source LLM from HuggingFace to allow you to ask questions based on specific information in a PDF. Nothing fancy, using 3rd party libs: HuggingFace, LanceDB, Langchain

### Future work

Idea is to extend this functionality to be used for any document that can be tokenized and "searched" through once put into a vector database. For the POC, I used the LOTR books and asked deep-cut questions, and it mostly(?) worked!

Could (in theory) be used by students to use an LLM to ask questions about subject material. Or just to be able to brainstorm with a document as context.

Web UI can be added as a front to upload any document. Creating an instance of LanceDB with all the chunks from the doc is the main bottle neck - for my local system, it took about 4-5 minutes everytime just for this operation. Once the backend has been modularised and some API endpoints have been written to do these operations, the UI should be trivial. 
