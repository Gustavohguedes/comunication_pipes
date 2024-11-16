import multiprocessing
import argparse
import unicodedata
import csv

def normalizar_texto(texto):
    """Remove acentuação e normaliza o texto."""
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')

def contar_palavras(bloco, palavra_chave, conn, indice_linha):
    """
    Conta o número de ocorrências de uma palavra-chave em um bloco de texto
    e identifica as linhas onde ocorre.
    """
    bloco_normalizado = normalizar_texto(bloco)
    palavra_chave_normalizada = normalizar_texto(palavra_chave)
    contador = bloco_normalizado.count(palavra_chave_normalizada)
    linhas_com_palavra = [
        indice_linha + i + 1 for i, linha in enumerate(bloco.split("\n"))
        if palavra_chave_normalizada in normalizar_texto(linha)
    ]
    conn.send((contador, linhas_com_palavra))  # Envia os resultados pelo pipe
    conn.close()  # Fecha o pipe

def salvar_relatorio(relatorio, formato, arquivo):
    """Salva o relatório em um arquivo no formato especificado."""
    if formato == "txt":
        with open(arquivo, "w") as f:
            f.write(relatorio)
    elif formato == "csv":
        with open(arquivo, "w", newline="") as f:
            writer = csv.writer(f)
            for linha in relatorio.split("\n"):
                writer.writerow([linha])

def main():
    # Configuração do argparse para receber argumentos
    parser = argparse.ArgumentParser(description="Contar palavras-chave em um arquivo de texto.")
    parser.add_argument("arquivo", type=str, help="Nome do arquivo a ser analisado")
    parser.add_argument("palavra_chave", type=str, help="Palavra-chave a ser buscada")
    parser.add_argument("--exportar", type=str, choices=["txt", "csv"], help="Exportar o relatório como txt ou csv")
    parser.add_argument("--saida", type=str, help="Nome do arquivo de saída (ex.: relatorio.txt)")

    args = parser.parse_args()

    # Lê o conteúdo do arquivo
    try:
        with open(args.arquivo, "r", encoding="utf-8") as f:
            texto = f.read()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{args.arquivo}' não foi encontrado.")
        return

    # Divide o texto em blocos
    blocos = texto.split("\n\n")  # Divide por parágrafos
    total_palavras = len(normalizar_texto(texto).split())  # Conta o total de palavras normalizadas no arquivo

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
    relatorio = (
        f"=== RELATÓRIO ===\n"
        f"Arquivo analisado: {args.arquivo}\n"
        f"Palavra-chave: '{args.palavra_chave}'\n"
        f"Total de palavras no arquivo: {total_palavras}\n"
        f"Número total de ocorrências: {total_ocorrencias}\n"
        f"Frequência relativa: {total_ocorrencias / total_palavras * 100:.2f}%\n"
    )
    if linhas_totais:
        relatorio += "Linhas contendo a palavra-chave: " + ", ".join(map(str, sorted(linhas_totais))) + "\n"
    else:
        relatorio += "A palavra-chave não foi encontrada no arquivo.\n"
    relatorio += "=================\n"

    # Imprime o relatório no console
    print(relatorio)

    # Exporta o relatório, se especificado
    if args.exportar and args.saida:
        salvar_relatorio(relatorio, args.exportar, args.saida)
        print(f"Relatório exportado para '{args.saida}' no formato {args.exportar.upper()}.")

if __name__ == "__main__":
    main()
