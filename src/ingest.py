import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
if not PDF_PATH:
    PDF_PATH = "document.pdf"
    
COLLECTION_NAME = "pdf_collection"
CONNECTION_STRING = os.getenv("DATABASE_URL")

def ingest_pdf():
    print("1. Carregando o PDF...")
    try:
        loader = PyPDFLoader(PDF_PATH)
        docs = loader.load()
    except Exception as e:
        print(f"Erro ao carregar o PDF. Verifique se o caminho '{PDF_PATH}' está correto. Erro: {e}")
        return

    print("2. Dividindo o documento (chunk_size=1000, overlap=150)...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    splits = text_splitter.split_documents(docs)
    print(f"   -> Foram gerados {len(splits)} chunks.")

    print("3. Conectando ao banco e gerando embeddings em lotes (para evitar Rate Limit)...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        pre_delete_collection=True
    )
    
    # Define o tamanho do lote para inserção no banco
    batch_size = 10
    
    for i in range(0, len(splits), batch_size):
        batch = splits[i : i + batch_size]
        
        vector_store.add_documents(batch)
        print(f"   -> Inseridos {min(i + batch_size, len(splits))} de {len(splits)} chunks...")
        
        if i + batch_size < len(splits):
            time.sleep(8)
            
    print("\nIngestão concluída com sucesso!")

if __name__ == "__main__":
    ingest_pdf()