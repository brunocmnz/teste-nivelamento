CREATE TABLE movimentos_contabeis (
    DATA DATE,
    REG_ANS INT(8),
    CD_CONTA_CONTABIL INT(8),
    DESCRICAO VARCHAR(150),
    VL_SALDO_INICIAL DECIMAL(10,2),
    VL_SALDO_FINAL DECIMAL(10,2)
);


CREATE TABLE operadoras (
    Registro_ANS VARCHAR(6) PRIMARY KEY,
    CNPJ VARCHAR(14) NOT NULL,
    Razao_Social VARCHAR(140) NOT NULL,
    Nome_Fantasia VARCHAR(140),
    Modalidade VARCHAR(2),
    Logradouro VARCHAR(40),
    Numero VARCHAR(20),
    Complemento VARCHAR(40),
    Bairro VARCHAR(30),
    Cidade VARCHAR(30),
    UF VARCHAR(2),
    CEP VARCHAR(8),
    DDD VARCHAR(4),
    Telefone VARCHAR(20),
    Fax VARCHAR(20),
    Endereco_eletronico VARCHAR(255),
    Representante VARCHAR(50),
    Cargo_Representante VARCHAR(40),
    Regiao_de_Comercializacao INT,
    Data_Registro_ANS DATE
);

