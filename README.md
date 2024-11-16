# comunication_pipes

<<<<<<< HEAD
# **Contador de Palavras-Chave com Comunicação entre Processos**

Este projeto é um programa em Python que utiliza **pipes** e **processos paralelos** para contar palavras-chave em um arquivo de texto. Além disso, oferece suporte à análise de arquivos com caracteres especiais ou acentos e permite exportar relatórios detalhados nos formatos `.txt` ou `.csv`.

#Integrantes
- Gustavo Henrique
- Bruno Vicente
- Igor Tenorio
- Franklin Roseveult

## **Funcionamento**

### **1. Leitura do Arquivo**
O programa lê o arquivo especificado no terminal, garantindo suporte a caracteres especiais e acentos utilizando codificação UTF-8.

### **2. Divisão em Blocos**
O texto é dividido em blocos para que cada bloco seja processado em paralelo. Por padrão, a divisão é feita por parágrafos (`\n\n`).

### **3. Contagem de Palavras**
Cada bloco é enviado para um processo filho, que:
- Normaliza o texto e a palavra-chave (remove acentos).
- Conta o número de ocorrências da palavra-chave.
- Identifica as linhas onde a palavra-chave aparece.

Os resultados são enviados de volta ao processo pai por meio de **pipes**.

### **4. Relatório Detalhado**
Após reunir os resultados de todos os processos, o programa gera um relatório contendo:
- Total de palavras no arquivo.
- Número total de ocorrências da palavra-chave.
- Frequência relativa da palavra-chave.
- Linhas onde a palavra-chave foi encontrada (se houver).

### **5. Exportação**
O relatório pode ser exportado nos formatos `.txt` ou `.csv`, com o nome do arquivo especificado pelo usuário.

---

## **Como Executar**

### **Dependências**
- Python 3.8 ou superior.
- Nenhuma biblioteca externa é necessária.


### **Exemplo**
No terminal, execute:
python contador_palavras.py texto.txt Python

### **Exportando um relatorio**
No Terminal, execute:
python contador_palavras.py texto.txt Python --exportar txt --saida relatorio.txt

### **Comando Básico**
No terminal, execute:
```bash
python contador_palavras.py <nome_do_arquivo> <palavra-chave>



=======
Autores

Franklin D. Alencar
>>>>>>> 52b0a727d4e6194dbb527cf5d39b0a485dbb445c
