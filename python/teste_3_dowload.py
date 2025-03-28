import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

# URL base
base_url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"

# Anos de interesse
anos_interesse = [2024, 2023]

pasta_destino = "downloads_t3"

# Função para fazer download de arquivos ZIP de um link
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


# Função principal para baixar os arquivos dos anos de interesse
def baixar_arquivos():
    for ano in anos_interesse:
        print(f"Baixando arquivos de {ano}...")
        baixar_arquivos_do_ano(ano)

# Chama a função principal
baixar_arquivos()
