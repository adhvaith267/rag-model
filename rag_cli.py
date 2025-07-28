from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain.schema import Document
from langchain_core.stores import InMemoryStore

from llama_cpp import Llama
from sentence_transformers import SentenceTransformer

from models import select_model
from select_docs import select_doc
from extract_docs_from_pdf import extract

pdf_path=select_doc()       #'works_policy_2016_1_2.pdf'
docs = extract(pdf_path)

child_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=30)
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=1000)

parent_docs = []
for i, doc in enumerate(docs):
    parent_docs.append(
            Document(
                page_content=doc,
                metadata={"parent_id": i}
            ))

# 5. Create child docs with matching parent_id
child_docs = []
for parent_doc in parent_docs:
    child_chunks = child_splitter.split_text(parent_doc.page_content)
    for chunk in child_chunks:
        child_docs.append(Document(
            page_content=chunk,
            metadata={"parent_id": parent_doc.metadata["parent_id"]}
        ))

embedding_model = HuggingFaceEmbeddings(model_name='/models/all-MiniLM-L6-v2')

vectorstore = FAISS.from_documents(parent_docs, embedding_model)

# 8. Create the new docstore
docstore = InMemoryStore()
# Add parent docs to store using parent_id
parent_doc_dict = {doc.metadata["parent_id"]: doc for doc in parent_docs}
docstore.mset(list(parent_doc_dict.items()))

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=docstore,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter
) 
# Step 4: Add documents to the retriever
retriever.add_documents(parent_docs)

llm = Llama(
    model_path=select_model(), #'/models/Mistral-7B-Instruct-v0.3.Q8_0/Mistral-7B-Instruct-v0.3.Q8_0.gguf',
    n_gpu_layers=2,
    temperature=0.1,
    n_threads=20,
    n_ctx = 8000,
    max_tokens = 8000,
    #generate_kwargs={},
    #verbose=True,
)

#print(llm(prompt="Use the following texts to keep in your context to answer following questions:" + "\n".join(docs), max_tokens=100, temperature=0.7, top_p=0.95)['choices'][0]['text'])
def ask(prompt):
    print("Generating...")
    return llm(prompt=prompt, max_tokens=500, temperature=0.7, top_p = 0.95, stop=["</s>"])['choices'][0]['text']

while(True):
    question = input("\nYour question please [Enter 'exit' to Exit]: ")
    if question.lower() == 'exit':
        break
    else:
        results =  retriever.invoke(question)
        context = "\n".join([doc.page_content for doc in results])
        #print(f"Question : {question} \n Context: {context}")

        prompt = f"""
        Answer the following question based on the given context.

        Context:
        {context}

        Question:
        {question}
        Answer:
        """
        prompt = f"[INST] Answer the question from the given context:\n\nContext: {context}\n\nQuestion: {question}\n\n[END]"
        response = ask(prompt)
        print(f"Response: {response}")
