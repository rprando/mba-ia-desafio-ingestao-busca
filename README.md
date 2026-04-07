# Desafio MBA Engenharia de Software com IA - Full Cycle

Este projeto implementa um pipeline RAG (Retrieval-Augmented Generation) para processar um arquivo PDF, armazenar suas informações de forma vetorial e permitir buscas contextuais via linha de comando (CLI). A solução garante que as respostas geradas sejam baseadas estritamente no conteúdo do documento fornecido.

## 🛠 Tecnologias Utilizadas

* **Linguagem:** Python
* **Framework:** LangChain
* **LLM e Embeddings:** Google Gemini (`gemini-2.5-flash-lite` e `gemini-embedding-001`)
* **Banco de Dados Vetorial:** PostgreSQL + extensão pgVector
* **Infraestrutura:** Docker e Docker Compose

## 📁 Estrutura do Projeto

```text
├── docker-compose.yml    # Configuração do banco de dados pgVector
├── requirements.txt      # Dependências Python
├── .env.example          # Template de variáveis de ambiente
├── src/
│   ├── ingest.py         # Script responsável pelo fatiamento e vetorização do PDF
│   ├── search.py         # Módulo de inicialização de recursos e busca de similaridade
│   ├── chat.py           # Interface de chat interativo via terminal (CLI)
├── document.pdf          # Arquivo PDF de origem dos dados
└── README.md             # Instruções do projeto
```

## ⚙️ Pré-requisitos

Para rodar este projeto localmente, você precisará ter instalado:
1. [Docker](https://docs.docker.com/get-docker/) e Docker Compose.
2. [Python 3.9+](https://www.python.org/downloads/).
3. Uma [Google API Key](https://aistudio.google.com/app/apikey) válida.

---

## 🚀 Como Executar o Projeto

### 1. Preparação do Ambiente

Clone o repositório e acesse a pasta raiz do projeto:

```bash
git clone https://github.com/rprando/mba-ia-desafio-ingestao-busca.git
cd mba-ia-desafio-ingestao-busca
```

Crie o arquivo de variáveis de ambiente a partir do template:

```bash
cp .env.example .env
```

Abra o arquivo `.env` e configure as variáveis com as suas credenciais e o nome do banco configurado no docker:

```env
GOOGLE_API_KEY=sua_chave_do_google_aqui
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PDF_PATH=document.pdf
```

### 2. Inicialização do Banco de Dados

Inicie o container do PostgreSQL com a extensão pgVector rodando o comando:

```bash
docker compose up -d
```
*(O script de inicialização do Docker garantirá que a extensão `vector` seja criada automaticamente).*

### 3. Instalação das Dependências (Python)

Crie um ambiente virtual para isolar as dependências:

```bash
python -m venv venv

# Ativação no Windows (Git Bash):
source venv/Scripts/activate

# Ativação no Linux/Mac:
source venv/bin/activate
```

Instale os pacotes necessários:

```bash
pip install -r requirements.txt
```
*Certifique-se de que o arquivo `document.pdf` está presente na raiz do projeto.*

### 4. Ingestão de Dados

Execute o script de ingestão. Este processo lerá o PDF, dividirá o texto em chunks e salvará os embeddings em lotes (batching) no banco de dados para evitar rate limits:

```bash
python src/ingest.py
```
*Aguarde a mensagem de "Ingestão concluída com sucesso!".*

### 5. Interação via CLI

Com os dados vetorizados, inicie o chat interativo no terminal:

```bash
python src/chat.py
```
*O assistente responderá às suas perguntas baseando-se unicamente nas informações contidas no PDF. Para encerrar o chat, basta digitar `sair` ou `exit`.*