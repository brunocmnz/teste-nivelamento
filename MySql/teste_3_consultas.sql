# Ultimo trimestre de 2024
WITH Ultimo_Trimestre AS (
    SELECT * 
    FROM movimentos_contabeis 
    WHERE descricao LIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS%'
    AND descricao LIKE '%ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
    AND Data BETWEEN '2024-10-01' AND '2024-12-31'
)
SELECT o.Registro_ANS, o.Nome_Fantasia, 
       u.VL_SALDO_INICIAL - u.VL_SALDO_FINAL AS DESPESA
FROM Ultimo_Trimestre u
JOIN operadoras o ON u.Reg_ANS = o.Registro_ANS
ORDER BY DESPESA DESC
LIMIT 10;

# Em 2024 inteiro
WITH Ultimo_Trimestre AS (
    SELECT * 
    FROM movimentos_contabeis 
    WHERE descricao LIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS%'
    AND descricao LIKE '%ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
    AND Data BETWEEN '2024-01-01' AND '2024-12-31'
)
SELECT o.Registro_ANS, o.Nome_Fantasia, 
       u.VL_SALDO_INICIAL - u.VL_SALDO_FINAL AS DESPESA
FROM Ultimo_Trimestre u
JOIN operadoras o ON u.Reg_ANS = o.Registro_ANS
ORDER BY DESPESA DESC
LIMIT 10;