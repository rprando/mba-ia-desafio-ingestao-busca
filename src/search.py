import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(question=None):
    """
    Inicializa os recursos (embeddings, db, llm) e retorna uma função que 
    executa a busca e gera a resposta.
    """
    try:
        CONNECTION_STRING = os.getenv("DATABASE_URL")
        COLLECTION_NAME = "pdf_collection"

        # Inicializa recursos de forma persistente (closure)
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        vector_store = PGVector(
            embeddings=embeddings,
            collection_name=COLLECTION_NAME,
            connection=CONNECTION_STRING,
        )
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)
        prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)

        def execute_chain(q: str):
            # 1. Busca os 10 resultados mais relevantes (k=10)
            results = vector_store.similarity_search_with_score(q, k=10)
            
            # 2. Extrai o texto dos chunks
            context_texts = [doc.page_content for doc, score in results]
            contexto_str = "\n\n".join(context_texts)
            
            # 3. Formata o prompt e aciona a LLM
            formatted_prompt = prompt.format(contexto=contexto_str, pergunta=q)
            resposta = llm.invoke(formatted_prompt)
            return resposta.content

        # Se uma pergunta foi passada diretamente, executa e retorna a string
        if question:
            return execute_chain(question)
        
        # Caso contrário, retorna a função inicializada para ser usada no loop do chat.py
        return execute_chain

    except Exception as e:
        print(f"Erro ao inicializar search_prompt: {e}")
        return None