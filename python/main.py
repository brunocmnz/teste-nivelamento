# Imports de web scraping
import requests
from bs4 import BeautifulSoup
import os

# Imports de compactacao
import zipfile
import os

# Função que compacta todos os arquivos dentro de uma pasta em um arquivo ZIP
def compactar_pasta(pasta_origem, zip_destino):
    """
        pasta_origem: Caminho da pasta que será compactada
        zip_destino: Nome do arquivo ZIP de saída
    """

    # Abre o arquivo ZIP no modo de escrita ("w"), sobrescrevendo caso já exista
    with zipfile.ZipFile(zip_destino, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Percorre a pasta de origem, incluindo subpastas e arquivos
        for root, _, files in os.walk(pasta_origem):
            # root -> Caminho atual da pasta sendo percorrida
            # _    -> Lista de subdiretórios (não utilizamos, por isso o "_")
            # files -> Lista de arquivos dentro da pasta atual

            for file in files:  # Itera sobre cada arquivo encontrado
                caminho_completo = os.path.join(root, file)  # Caminho absoluto do arquivo
                # Converte para caminho relativo para manter a estrutura da pasta dentro do ZIP
                caminho_relativo = os.path.relpath(caminho_completo, pasta_origem)

                zipf.write(caminho_completo, caminho_relativo)  # Adiciona o arquivo ao ZIP
                print(f"Adicionado: {caminho_relativo}")  # Exibe os arquivos adicionados ao ZIP

# URL da página que contém os anexos
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

# Criar pasta para armazenar os arquivos
os.makedirs("downloads", exist_ok=True)

# Cabeçalhos para simular um navegador real (evita bloqueios)
headers = {"User-Agent": "Mozilla/5.0"}

# Requisição para obter o conteúdo da página
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Encontra os links dos anexos (exemplo: arquivos .pdf)
for link in soup.find_all("a", href=True):
    file_url = link["href"]

    # Filtra apenas links com arquivos desejados (pdf e "Anexo")
    if link.text.__contains__("Anexo") and file_url.endswith(".pdf"):
        file_name = file_url.split("/")[-1]  # Extrai o nome do arquivo

        # Baixa o arquivo
        file_response = requests.get(file_url, headers=headers)
        with open(f"downloads/{file_name}", "wb") as file:
            file.write(file_response.content)

        print(f"Baixado: {file_name}")

print("Download concluído!")

# Nome da pasta que será compactada
pasta_origem = "downloads"
# Nome do arquivo zip
zip_destino = "arquivos_comprimidos.zip"

# Chamar a função para compactar
compactar_pasta(pasta_origem, zip_destino)

print(f"Pasta '{pasta_origem}' compactada como '{zip_destino}'")
