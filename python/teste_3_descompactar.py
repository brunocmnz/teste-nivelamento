import os
import zipfile
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import pandas as pd

# URL base
base_url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
base_url_csv = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/"

# Anos de interesse
anos_interesse = [2024, 2023]

pasta_destino = "dowloads_t3"


# Função para fazer download de arquivos
def baixar_arquivo(url, pasta_destino):
    resposta = requests.get(url)
    nome_arquivo = os.path.basename(url)
    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

    with open(caminho_arquivo, 'wb') as f:
        f.write(resposta.content)
    print(f"Arquivo {nome_arquivo} baixado!")


# Função para obter os links dos arquivos zip de um ano específico
def obter_links_ano(ano):
    resposta = requests.get(base_url)
    soup = BeautifulSoup(resposta.text, 'html.parser')

    # Encontrar todos os links na página
    links = soup.find_all('a', href=True)
    links_ano = []

    for link in links:
        href = link['href']
        # Verifica se o link contém o ano de interesse e é um link para um diretório
        if str(ano) in href and href.endswith('/'):
            links_ano.append(urljoin(base_url, href))

    return links_ano


# Função para baixar arquivos ZIP de um link de ano específico
def baixar_arquivos_do_ano(ano):
    # Cria uma pasta para salvar os arquivos do ano
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    # Obtém os links das pastas do ano
    links = obter_links_ano(ano)

    for link in links:
        print(f"Acessando: {link}")
        resposta = requests.get(link)
        soup = BeautifulSoup(resposta.text, 'html.parser')

        # Encontrar todos os links de arquivos ZIP dentro do diretório
        zip_links = soup.find_all('a', href=re.compile(r'.*\.zip$'))

        for zip_link in zip_links:
            zip_url = urljoin(link, zip_link['href'])
            baixar_arquivo(zip_url, pasta_destino)


# Função para baixar arquivos CSV de um link específico
def baixar_arquivos_csv():
    resposta = requests.get(base_url_csv)
    soup = BeautifulSoup(resposta.text, 'html.parser')

    # Encontrar todos os links na página
    links = soup.find_all('a', href=True)

    for link in links:
        href = link['href']
        # Verifica se o link contém a extensão .csv
        if href.endswith('.csv'):
            csv_url = urljoin(base_url_csv, href)
            baixar_arquivo(csv_url, pasta_destino)


# Função para descompactar arquivos ZIP na pasta de destino
def descompactar_arquivos(pasta_destino):
    # Verifica todos os arquivos na pasta de destino
    for arquivo in os.listdir(pasta_destino):
        caminho_arquivo = os.path.join(pasta_destino, arquivo)

        # Verifica se é um arquivo ZIP
        if zipfile.is_zipfile(caminho_arquivo):
            print(f"Descompactando: {arquivo}")
            with zipfile.ZipFile(caminho_arquivo, 'r') as zip_ref:
                # Extrai os arquivos para a pasta de destino
                zip_ref.extractall(pasta_destino)
            print(f"Arquivo {arquivo} descompactado com sucesso!")


# Função para combinar arquivos CSV em um único arquivo
def combinar_csv(pasta_csv_destino, arquivo_saida):
    # Cria um DataFrame vazio para acumular os dados
    dados_combinados = pd.DataFrame()

    # Itera sobre os arquivos CSV na pasta
    for arquivo in os.listdir(pasta_csv_destino):
        if arquivo.endswith('.csv'):
            caminho_arquivo = os.path.join(pasta_csv_destino, arquivo)
            print(f"Lendo o arquivo CSV: {caminho_arquivo}")

            try:
                # Tenta ler o arquivo CSV com diferentes separadores
                df = pd.read_csv(caminho_arquivo, sep=';', engine='python', on_bad_lines='skip')
                if df.empty:
                    print(f"O arquivo {arquivo} está vazio ou não possui dados válidos.")
                else:
                    print(f"Dados lidos do arquivo {arquivo}:")
                    print(df.head())  # Imprime as primeiras linhas para depuração
                dados_combinados = pd.concat([dados_combinados, df], ignore_index=True)
            except Exception as e:
                print(f"Erro ao ler o arquivo {arquivo}: {e}")

    if dados_combinados.empty:
        print("Nenhum dado foi combinado. Verifique os arquivos CSV baixados.")
    else:
        # Salva os dados combinados em um novo arquivo CSV
        dados_combinados.to_csv(arquivo_saida, index=False)
        print(f"Arquivo combinado salvo em: {arquivo_saida}")


# Função principal para baixar, descompactar e combinar os arquivos
def processar_arquivos(baixar=True, descompactar=True, combinar=True):
    if baixar:
        for ano in anos_interesse:
            print(f"Baixando arquivos de {ano}...")
            baixar_arquivos_do_ano(ano)
        # Baixar arquivos CSV de operadoras de plano de saúde
        print("Baixando arquivos CSV de operadoras de plano de saúde...")
        baixar_arquivos_csv()

    if descompactar:
        # Após o download, descompacta os arquivos
        print("Descompactando os arquivos baixados...")
        descompactar_arquivos(pasta_destino)

    if combinar:
        # Combinar os arquivos CSV em um único arquivo "movimentacoes.csv"
        arquivo_saida = os.path.join(pasta_destino, "movimentacoes.csv")
        print("Combinando os arquivos CSV...")
        combinar_csv(pasta_destino, arquivo_saida)


# Chama a função principal
processar_arquivos(False, False, True)
