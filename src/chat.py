from search import search_prompt

def main():
    print("Inicializando as conexões com Banco e LLM...")
    
    # Recebe a função 'execute_chain' já com os recursos em memória
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    print("\nChatbot iniciado com sucesso! (Digite 'sair' para encerrar)")
    
    while True:
        pergunta = input("\nVocê: ")
        
        # Condição de saída
        if pergunta.strip().lower() in ['sair', 'exit', 'quit']:
            print("Encerrando a aplicação.")
            break
        
        if not pergunta.strip():
            continue

        try:
            # Chama a função gerada no search_prompt passando a pergunta
            resposta = chain(pergunta)
            print(f"\nAssistente: {resposta}")
        except Exception as e:
            print(f"\n[Erro na geração da resposta]: {e}")

if __name__ == "__main__":
    main()