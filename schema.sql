CREATE TABLE ESTOQUE (
    CODIGO INTEGER PRIMARY KEY AUTOINCREMENT,  -- CODIGO será auto-incrementado
    ITEM TEXT NOT NULL UNIQUE,
    PESO TEXT NOT NULL,
    QUANTIDADE INTEGER NOT NULL,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Data de atualização padrão
    CONSTRAINT check_quantidade_non_negative CHECK (QUANTIDADE >= 0)
);

-- Inserção dos dados na tabela ESTOQUE
INSERT INTO ESTOQUE (ITEM, PESO, QUANTIDADE) VALUES ('Açucar', '1 kg', 0);
INSERT INTO ESTOQUE (ITEM, PESO, QUANTIDADE) VALUES ('Arroz', '5 kg', 0);
INSERT INTO ESTOQUE (ITEM, PESO, QUANTIDADE) VALUES ('Biscoito Doce', '1 pacote', 0);
INSERT INTO ESTOQUE (ITEM, PESO, QUANTIDADE) VALUES ('Biscoito Salgado', '1 pacote', 0);
INSERT INTO ESTOQUE (ITEM, PESO, QUANTIDADE) VALUES ('Cafe', '500 gr', 0);
INSERT INTO ESTOQUE (ITEM, PESO, QUANTIDADE) VALUES ('Creme Dental', '1 pacote', 0);
INSERT INTO ESTOQUE (ITEM, PESO, QUANTIDADE) VALUES ('Farinha de Mandioca', '500 gr', 0);
INSERT INTO ESTOQUE (ITEM, PESO, QUANTIDADE) VALUES ('Farinha de Trigo', '1 kg', 0);
INSERT INTO ESTOQUE (ITEM, PESO, QUANTIDADE) VALUES ('Feijao', '1 kg', 0);
INSERT INTO ESTOQUE (ITEM, PESO, QUANTIDADE) VALUES ('Macarrao', '500 gr', 0);
INSERT INTO ESTOQUE (ITEM, PESO, QUANTIDADE) VALUES ('Molho de Tomate', '1 pacote', 0);
INSERT INTO ESTOQUE (ITEM, PESO, QUANTIDADE) VALUES ('Oleo', '900 ml', 0);
INSERT INTO ESTOQUE (ITEM, PESO, QUANTIDADE) VALUES ('Sabonete', '1 un', 0);
INSERT INTO ESTOQUE (ITEM, PESO, QUANTIDADE) VALUES ('Sal', '1 kg', 0);

CREATE TABLE CESTABASE (
    CHAVE INTEGER PRIMARY KEY AUTOINCREMENT,  -- CHAVE será auto-incrementada
    ITEM TEXT NOT NULL UNIQUE,
    PESO TEXT NOT NULL,
    QUANTIDADE INTEGER NOT NULL,
    CONSTRAINT check_quantidade_nao_negativa CHECK (QUANTIDADE >= 0)
);

-- Inserção dos dados na tabela CESTABASE
INSERT INTO CESTABASE (ITEM, PESO, QUANTIDADE) VALUES ('Acucar', '1 kg', 2);
INSERT INTO CESTABASE (ITEM, PESO, QUANTIDADE) VALUES ('Arroz', '5 kg', 1);
INSERT INTO CESTABASE (ITEM, PESO, QUANTIDADE) VALUES ('Biscoito Doce', '1 pacote', 1);
INSERT INTO CESTABASE (ITEM, PESO, QUANTIDADE) VALUES ('Biscoito Salgado', '1 pacote', 1);
INSERT INTO CESTABASE (ITEM, PESO, QUANTIDADE) VALUES ('Cafe', '500 gr', 1);
INSERT INTO CESTABASE (ITEM, PESO, QUANTIDADE) VALUES ('Creme Dental', '1 pacote', 1);
INSERT INTO CESTABASE (ITEM, PESO, QUANTIDADE) VALUES ('Farinha de Mandioca', '500 gr', 1);
INSERT INTO CESTABASE (ITEM, PESO, QUANTIDADE) VALUES ('Farinha de Trigo', '1 kg', 1);
INSERT INTO CESTABASE (ITEM, PESO, QUANTIDADE) VALUES ('Feijao', '1 kg', 2);
INSERT INTO CESTABASE (ITEM, PESO, QUANTIDADE) VALUES ('Macarrao', '500 gr', 2);
INSERT INTO CESTABASE (ITEM, PESO, QUANTIDADE) VALUES ('Molho de Tomate', '1 pacote', 2);
INSERT INTO CESTABASE (ITEM, PESO, QUANTIDADE) VALUES ('Oleo', '900 ml', 1);
INSERT INTO CESTABASE (ITEM, PESO, QUANTIDADE) VALUES ('Sabonete', '1 un', 2);
INSERT INTO CESTABASE (ITEM, PESO, QUANTIDADE) VALUES ('Sal', '1 kg', 1);
