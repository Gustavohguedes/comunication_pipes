import multiprocessing
import argparse

def contar_palavras(bloco, palavra_chave, conn, indice_linha):
    """
    Conta o número de ocorrências de uma palavra-chave em um bloco de texto
    e identifica as linhas onde ocorre.
    """
    contador = bloco.count(palavra_chave)
    linhas_com_palavra = [indice_linha + i + 1 for i, linha in enumerate(bloco.split("\n")) if palavra_chave in linha]
    conn.send((contador, linhas_com_palavra))  # Envia os resultados pelo pipe
    conn.close()  # Fecha o pipe

def main():
    # Configuração do argparse para receber o nome do arquivo e a palavra-chave
    parser = argparse.ArgumentParser(description="Contar palavras-chave em um arquivo de texto.")
    parser.add_argument("arquivo", type=str, help="Nome do arquivo a ser analisado")
    parser.add_argument("palavra_chave", type=str, help="Palavra-chave a ser buscada")

    args = parser.parse_args()

    # Lê o conteúdo do arquivo
    try:
        with open(args.arquivo, "r") as f:
            texto = f.read()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{args.arquivo}' não foi encontrado.")
        return

    # Divide o texto em blocos (exemplo: por parágrafos)
    blocos = texto.split("\n\n")  # Divide por parágrafos
    total_palavras = len(texto.split())  # Conta o total de palavras no arquivo

    processos = []
    pipes = []

    # Cria processos para contar palavras em cada bloco
    for indice, bloco in enumerate(blocos):
        pai_conn, filho_conn = multiprocessing.Pipe()  # Cria um par de conexões do pipe
        processo = multiprocessing.Process(
            target=contar_palavras, args=(bloco, args.palavra_chave, filho_conn, indice * len(bloco.split("\n")))
        )
        processos.append(processo)
        pipes.append(pai_conn)
        processo.start()

    # Recolhe os resultados dos processos filhos
    total_ocorrencias = 0
    linhas_totais = set()
    for pipe in pipes:
        ocorrencias, linhas = pipe.recv()  # Recebe a contagem e as linhas
        total_ocorrencias += ocorrencias
        linhas_totais.update(linhas)

    # Aguarda o término de todos os processos
    for processo in processos:
        processo.join()

    # Gera o relatório
    print("\n=== RELATÓRIO ===")
    print(f"Arquivo analisado: {args.arquivo}")
    print(f"Palavra-chave: '{args.palavra_chave}'")
    print(f"Total de palavras no arquivo: {total_palavras}")
    print(f"Número total de ocorrências: {total_ocorrencias}")
    print(f"Frequência relativa: {total_ocorrencias / total_palavras * 100:.2f}%")
    if linhas_totais:
        print("Linhas contendo a palavra-chave:", sorted(linhas_totais))
    else:
        print("A palavra-chave não foi encontrada no arquivo.")
    print("=================\n")

if __name__ == "__main__":
    main()
