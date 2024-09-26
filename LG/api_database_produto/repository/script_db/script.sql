-- 1. Remover o banco de dados se já existir
DROP DATABASE IF EXISTS banco;

-- 2. Criar o banco de dados
CREATE DATABASE banco;

-- 3. Conceder permissões para o usuário root
GRANT ALL PRIVILEGES ON banco.* TO 'root'@'localhost';

-- 4. Usar o banco de dados criado
USE banco;

-- 5. Criar a tabela 'produto'
CREATE TABLE produto (
    id INT AUTO_INCREMENT,               -- Chave primária auto-incrementada
    descricao VARCHAR(50) NOT NULL,      -- Descrição do produto
    unidade VARCHAR(5) NOT NULL,         -- Unidade de medida do produto
    quantidade DECIMAL(10,2) NOT NULL,   -- Quantidade do produto
    preco_real DECIMAL(10,2) NOT NULL,   -- Preço em Reais
    preco_dolar DECIMAL(10,2) NOT NULL,  -- Preço em Dólar (será atualizado depois)
    PRIMARY KEY (id)                     -- Chave primária na coluna 'id'
);