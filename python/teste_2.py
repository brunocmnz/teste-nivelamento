import pdfplumber
import pandas as pd
import zipfile
import os

# Definição dos arquivos
pdf_file = "downloads/anexo_1.pdf"  # Substitua pelo nome correto do PDF
csv_file = "Rol_de_Procedimentos.csv"
zip_file = "Teste_2_csv.zip"  # Substitua pelo seu nome

# Legenda para substituição das abreviações
substituicoes = {
    "OD": "Seg. Odontológica",
    "AMB": "Seg. Ambulatorial"
}

# Função para extrair e processar os dados
def extrair_dados():
    dados_extraidos = []
    with pdfplumber.open(pdf_file) as pdf:
        # Tenta extrair a tabela da primeira página
        tabelas = pdf.pages[0].extract_tables()

        if tabelas:  # Verifica se existe alguma tabela
            for tabela in tabelas:
                if tabela:  # Garante que a tabela não está vazia
                    for linha in tabela:
                        linha_limpa = [str(celula).strip() if celula is not None else "" for celula in linha]
                        dados_extraidos.append(linha_limpa)

        # Processa as tabelas a partir da terceira página
        for i in range(2, len(pdf.pages)):  # A partir da terceira página (índice 2)
            tabelas = pdf.pages[i].extract_tables()
            for tabela in tabelas:
                if tabela:  # Garante que a tabela não está vazia
                    for linha in tabela:
                        linha_limpa = [str(celula).strip() if celula is not None else "" for celula in linha]
                        dados_extraidos.append(linha_limpa)

    return dados_extraidos

# Função principal para processar e salvar os dados
def processar_pdf():
    # Extrair os dados
    dados_extraidos = extrair_dados()

    # Verifica se há dados extraídos
    if dados_extraidos:
        # Converte para DataFrame do Pandas
        df = pd.DataFrame(dados_extraidos)

        # Substitui os cabeçalhos
        df.columns = df.iloc[0].map(lambda x: substituicoes.get(x, x))  # Aplica substituição nos cabeçalhos
        df = df[1:].reset_index(drop=True)  # Remove a primeira linha com os cabeçalhos originais

        # Substitui as abreviações em toda a tabela (incluindo os dados)
        df = df.apply(lambda x: x.map(lambda y: substituicoes.get(y, y) if isinstance(y, str) else y))

        # Salva os dados em CSV (formato melhor para Excel)
        df.to_csv(csv_file, index=False, sep=";", encoding="utf-8-sig")

        # Compacta o CSV em um arquivo ZIP
        with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_file, os.path.basename(csv_file))  # Adiciona ao ZIP sem o caminho completo

        # Remove o CSV original após compactação (opcional)
        os.remove(csv_file)

        print(f"Arquivo {zip_file} criado com sucesso!")
    else:
        print("Nenhuma tabela foi encontrada no PDF.")

# Inicia o processamento
processar_pdf()
