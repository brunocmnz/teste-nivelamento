import pandas as pd
import mysql.connector
from mysql.connector import Error
from concurrent.futures import ThreadPoolExecutor

# Função para inserir dados no MySQL
def inserir_dados_mysql(caminho_csv, tabela):
    cursor = None  # Inicializa cursor como None
    try:
        # Conectar ao banco de dados MySQL
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Adicione sua senha aqui, se necessário
            database='teste_3'
        )

        if conexao.is_connected():
            print(f'Conectado ao MySQL. Inserindo dados na tabela {tabela}...')

            # Ler o arquivo CSV para um DataFrame do Pandas
            df = pd.read_csv(caminho_csv, sep=';', encoding='utf-8')

            # Verificar o formato da data e converter, se necessário
            if df['DATA'].str.contains('-').any():  # Verifica se já está no formato ISO
                df['DATA'] = pd.to_datetime(df['DATA'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
            else:
                df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

            # Substituir vírgulas por pontos para as colunas que devem ser números decimais
            for col in ['VL_SALDO_INICIAL', 'VL_SALDO_FINAL']:  # Colunas de valores decimais
                df[col] = df[col].str.replace(',', '.', regex=False).astype(float)

            # Criar um cursor
            cursor = conexao.cursor()

            # Loop pelos dados e inserir linha por linha
            for i, row in df.iterrows():
                # Cria a consulta de inserção dinâmica
                sql = f"INSERT INTO {tabela} ({', '.join(df.columns)}) VALUES ({', '.join(['%s'] * len(row))})"
                cursor.execute(sql, tuple(row))

            # Commit as alterações
            conexao.commit()
            print(f'Dados inseridos com sucesso na tabela {tabela}!')

    except FileNotFoundError as fnf_error:
        print(f"Erro: Arquivo não encontrado - {fnf_error}")
    except Error as e:
        print(f'Erro na conexão ou execução SQL: {e}')

    finally:
        # Verifica se o cursor foi criado antes de tentar fechá-lo
        if cursor:
            cursor.close()
        if conexao.is_connected():
            conexao.close()

# Lista de arquivos e tabelas
arquivos_csv = [
    'C:/Users/bruno/AppData/Local/GitHubDesktop/app-3.3.3/teste-nivelamento/python/downloads_t3/1T2023.csv',
    'C:/Users/bruno/AppData/Local/GitHubDesktop/app-3.3.3/teste-nivelamento/python/downloads_t3/2T2023.csv',
    'C:/Users/bruno/AppData/Local/GitHubDesktop/app-3.3.3/teste-nivelamento/python/downloads_t3/3T2023.csv',
    'C:/Users/bruno/AppData/Local/GitHubDesktop/app-3.3.3/teste-nivelamento/python/downloads_t3/4T2023.csv',
    'C:/Users/bruno/AppData/Local/GitHubDesktop/app-3.3.3/teste-nivelamento/python/downloads_t3/1T2024.csv',
    'C:/Users/bruno/AppData/Local/GitHubDesktop/app-3.3.3/teste-nivelamento/python/downloads_t3/2T2024.csv',
    'C:/Users/bruno/AppData/Local/GitHubDesktop/app-3.3.3/teste-nivelamento/python/downloads_t3/3T2024.csv',
    'C:/Users/bruno/AppData/Local/GitHubDesktop/app-3.3.3/teste-nivelamento/python/downloads_t3/4T2024.csv'
]

tabela = 'movimentos_contabeis'

# Função para executar a inserção com multithreading
def inserir_em_multithread():
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(inserir_dados_mysql, arquivo, tabela) for arquivo in arquivos_csv]
        # Aguarda todas as threads terminarem
        for future in futures:
            future.result()

# Chama a função para iniciar o processo
inserir_em_multithread()
