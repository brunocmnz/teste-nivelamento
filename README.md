# teste-nivelamento
Teste de nivelamento com manipulação de dados, programação, Python e SQL.

## Teste 1
O código faz o dowload corretamente dos dados desejados, bem como a compactação dos arquivos em zip.
O código *teste_1.py* faz o dowload dos anexos na pasta *downloads_t1*, que é criada, caso não exista. Após isso, é feito a compactação dos anexos, na pasta principal no formato zip.

## Teste 2
Poderia utilizar Threds para agilizar o processo, mas como não era um volume muito grande de dados, fiz do jeito tradicional. Caso fosse utilizado threads, poderia haver uma desordenação dos dados, e seria preciso então lidar com isso e fazer a ordenação caso fosse necessário.
O código *teste_2.py* faz o compilado dos dados desejados que estão no pdf do anexo 1, unificando-os em um único arquivo e compactando esse arquivo na pasta principal como *Teste_2_csv.zip* .

## Teste 3
Foram criados os códigos, baixando os arquivos, descompactando os arquivos baixados e inserindo os dados no MySql. Após isso, foram criadas as consultas no MySql para resultar nos dados desejados.
Os códigos criados nesse teste foram:
- *teste_3_download.py :* Faz o download dos arquivos desejados (últimos dois anos, 2023 e 2024) na pasta *downloads_t1*.
- *teste_3_descompactar.py: * Descompacta os arquivos baixados na pasta *downloads_t1*
- *teste_3_insert_movimentacoes.py :* Insere os dados obtidos na tabela *movimentos_contabeis*.
- *teste_3_insert_operadoras.py :* Insere os dados obtidos na tabela *operadoras*.
