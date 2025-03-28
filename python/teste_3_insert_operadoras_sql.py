import pandas as pd
import mysql.connector
from mysql.connector import Error

# Função para inserir dados no MySQL
def inserir_dados_operadoras(caminho_csv, tabela):
    cursor = None
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
            df = pd.read_csv(caminho_csv, sep=';', encoding='utf-8', dtype=str)

            # Substituir NaN por None
            df = df.map(lambda x: None if pd.isna(x) or str(x).strip().lower() in ['nan', 'none', ''] else x)

            # Truncar valores da coluna Modalidade (max 2 caracteres)
            if 'Modalidade' in df.columns:
                df['Modalidade'] = df['Modalidade'].astype(str).str[:2]

                # Verificar se algum dado foi cortado
                valores_originais = df['Modalidade'].dropna().unique()
                valores_truncados = df['Modalidade'].dropna().unique()
                if any(len(v) > 2 for v in valores_originais):
                    print("⚠️ Atenção: Alguns valores da coluna 'Modalidade' foram truncados para 2 caracteres!")

            # Converter Data_Registro_ANS para formato MySQL
            if 'Data_Registro_ANS' in df.columns:
                df['Data_Registro_ANS'] = pd.to_datetime(df['Data_Registro_ANS'], format='%d/%m/%Y', errors='coerce').dt.strftime('%Y-%m-%d')
                df['Data_Registro_ANS'] = df['Data_Registro_ANS'].replace({pd.NaT: None})  # Substituir NaT por None

            # Garantir que colunas numéricas não tenham valores NaN
            colunas_numericas = ['Regiao_de_Comercializacao']
            for col in colunas_numericas:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

            # Criar um cursor
            cursor = conexao.cursor()

            # Loop pelos dados e inserir linha por linha
            for _, row in df.iterrows():
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
        if cursor:
            cursor.close()
        if conexao.is_connected():
            conexao.close()

# Caminho do arquivo e nome da tabela
arquivo_csv = 'C:/Users/bruno/AppData/Local/GitHubDesktop/app-3.3.3/teste-nivelamento/python/downloads_t3/Relatorio_cadop.csv'
tabela = 'operadoras'

# Inserir os dados no banco
inserir_dados_operadoras(arquivo_csv, tabela)
