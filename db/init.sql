CREATE DATABASE IF NOT EXISTS mecanica;
USE mecanica;

CREATE TABLE Clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(30),
    email VARCHAR(100),
    endereco VARCHAR(255),
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Veiculos (
    id_veiculo INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    placa VARCHAR(10) NOT NULL,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    ano INT,
    cor VARCHAR(30),
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente)
);

CREATE TABLE Servicos (
    id_servico INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(255) NOT NULL,
    preco_base DECIMAL(10,2) NOT NULL,
    tempo_estimado VARCHAR(20)
);

CREATE TABLE Produtos (
    id_produto INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255),
    preco_venda DECIMAL(10,2) NOT NULL,
    quantidade_estoque INT DEFAULT 0
);

CREATE TABLE Funcionarios (
    id_funcionario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cargo VARCHAR(50),
    salario DECIMAL(10,2),
    data_admissao DATE
);

CREATE TABLE Ordens_de_Servico (
    id_os INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_veiculo INT NOT NULL,
    data_entrada DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_saida DATETIME,
    status VARCHAR(30) DEFAULT 'Aberta',
    observacoes TEXT,
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente),
    FOREIGN KEY (id_veiculo) REFERENCES Veiculos(id_veiculo)
);

CREATE TABLE Servicos_OS (
    id_os INT NOT NULL,
    id_servico INT NOT NULL,
    valor_cobrado DECIMAL(10,2),
    quantidade INT DEFAULT 1,
    PRIMARY KEY (id_os, id_servico),
    FOREIGN KEY (id_os) REFERENCES Ordens_de_Servico(id_os),
    FOREIGN KEY (id_servico) REFERENCES Servicos(id_servico)
);

CREATE TABLE Produtos_OS (
    id_os INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT DEFAULT 1,
    valor_unitario DECIMAL(10,2),
    PRIMARY KEY (id_os, id_produto),
    FOREIGN KEY (id_os) REFERENCES Ordens_de_Servico(id_os),
    FOREIGN KEY (id_produto) REFERENCES Produtos(id_produto)
);

CREATE TABLE Funcionarios_OS (
    id_os INT NOT NULL,
    id_funcionario INT NOT NULL,
    funcao_na_os VARCHAR(100),
    PRIMARY KEY (id_os, id_funcionario),
    FOREIGN KEY (id_os) REFERENCES Ordens_de_Servico(id_os),
    FOREIGN KEY (id_funcionario) REFERENCES Funcionarios(id_funcionario)
);

CREATE TABLE Pagamentos (
    id_pagamento INT AUTO_INCREMENT PRIMARY KEY,
    id_os INT NOT NULL,
    valor_total DECIMAL(10,2) NOT NULL,
    forma_pagamento VARCHAR(50),
    data_pagamento DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(30) DEFAULT 'Pendente',
    FOREIGN KEY (id_os) REFERENCES Ordens_de_Servico(id_os)
);
