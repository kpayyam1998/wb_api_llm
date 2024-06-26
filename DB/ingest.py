"""
In this file implementation which is help to store vectors in FAISS DB

"""

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

DIR_PATH="../pdfdoc/"
DB_FAISS_PATH="../vectorstores/db_faiss/"

os.makedirs(DIR_PATH,exist_ok=True)
os.makedirs(DB_FAISS_PATH,exist_ok=True)
api_key=os.environ.get('OPEIAI_API_KEY')
#----------------------------------------------------------------
# FAISS DB
#----------------------------------------------------------------

def create_vectordb():
    try:
        #Load file
        loader=DirectoryLoader(DIR_PATH,glob="*.pdf",loader_cls=PyPDFLoader)
        documents=loader.load()

        #split chunks of documents
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
        docs=text_splitter.split_documents(documents)

        #embedding
        embeddings=OpenAIEmbeddings(api_key=api_key)

        #vectorstore
        vector_store_db=FAISS.from_documents(docs,embeddings)
        vector_store_db.save_local(DB_FAISS_PATH)
    except Exception as e:
        raise FileNotFoundError(e)
    
# if __name__ == "__main__":
#      create_vectordb()