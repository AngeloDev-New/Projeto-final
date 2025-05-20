import mysql.connector
import time
from faker import Faker
import random
localhost = "127.0.0.1"

fake = Faker()

MAX_DB_SIZE_MB = 3600  # 3GB = 3600MB aproximadamente

def wait_for_mysql():
    for i in range(30):
        try:
            con = mysql.connector.connect(
                host=localhost,
                port=4600,
                user="user",
                password="pass",
                database="mecanica"
            )
            con.close()
            print("✅ Conexão com MySQL estabelecida.")
            return
        except Exception:
            print(f"Aguardando MySQL... ({i+1}/30)")
            time.sleep(2)
    raise Exception("⛔ Timeout: MySQL não respondeu após 60s.")

def get_db_size_mb(cursor):
    cursor.execute("""
        SELECT 
            ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS size_mb
        FROM 
            information_schema.tables
        WHERE 
            table_schema = 'mecanica';
    """)
    size_mb = cursor.fetchone()[0]
    return size_mb or 0

def insert_clientes(cursor, n):
    for _ in range(n):
        nome = fake.name()
        telefone = fake.phone_number()
        email = fake.email()
        endereco = fake.address().replace("\n", ", ")
        cursor.execute(
            "INSERT INTO Clientes (nome, telefone, email, endereco) VALUES (%s, %s, %s, %s)",
            (nome, telefone, email, endereco)
        )

def insert_veiculos(cursor, n, clientes_ids):
    marcas = ['Ford', 'Chevrolet', 'Volkswagen', 'Fiat', 'Toyota', 'Honda']
    cores = ['Preto', 'Branco', 'Vermelho', 'Azul', 'Prata']
    for _ in range(n):
        id_cliente = random.choice(clientes_ids)
        placa = fake.license_plate()
        marca = random.choice(marcas)
        modelo = fake.word().capitalize()
        ano = random.randint(1990, 2025)
        cor = random.choice(cores)
        cursor.execute(
            "INSERT INTO Veiculos (id_cliente, placa, marca, modelo, ano, cor) VALUES (%s, %s, %s, %s, %s, %s)",
            (id_cliente, placa, marca, modelo, ano, cor)
        )

def insert_servicos(cursor, n=100):
    for _ in range(n):
        descricao = fake.sentence(nb_words=6)
        preco_base = round(random.uniform(50, 1500), 2)
        tempo_estimado = f"{random.randint(1, 10)}h"
        cursor.execute(
            "INSERT INTO Servicos (descricao, preco_base, tempo_estimado) VALUES (%s, %s, %s)",
            (descricao, preco_base, tempo_estimado)
        )

def insert_produtos(cursor, n=100):
    for _ in range(n):
        nome = fake.word().capitalize()
        descricao = fake.sentence(nb_words=8)
        preco_venda = round(random.uniform(10, 500), 2)
        quantidade_estoque = random.randint(0, 1000)
        cursor.execute(
            "INSERT INTO Produtos (nome, descricao, preco_venda, quantidade_estoque) VALUES (%s, %s, %s, %s)",
            (nome, descricao, preco_venda, quantidade_estoque)
        )

def insert_funcionarios(cursor, n=100):
    cargos = ['Mecânico', 'Gerente', 'Atendente', 'Eletricista', 'Encarregado']
    for _ in range(n):
        nome = fake.name()
        cargo = random.choice(cargos)
        salario = round(random.uniform(1500, 7000), 2)
        data_admissao = fake.date_between(start_date='-5y', end_date='today')
        cursor.execute(
            "INSERT INTO Funcionarios (nome, cargo, salario, data_admissao) VALUES (%s, %s, %s, %s)",
            (nome, cargo, salario, data_admissao)
        )

def main():
    wait_for_mysql()

    con = mysql.connector.connect(
        host=localhost,
        port=4600,
        user="user",
        password="pass",
        database="mecanica"
    )
    cursor = con.cursor()

    while True:
        size_mb = get_db_size_mb(cursor)
        print(f"Tamanho do banco atual: {size_mb} MB")
        if size_mb >= MAX_DB_SIZE_MB:
            print("🚦 Limite de tamanho do banco atingido. Parando inserções.")
            break

        # Insere lotes de dados
        insert_clientes(cursor, 1000)
        con.commit()

        # Busca os IDs dos clientes para inserir veículos (para simplificar só os últimos 1000 inseridos)
        cursor.execute("SELECT id_cliente FROM Clientes ORDER BY id_cliente DESC LIMIT 1000")
        clientes_ids = [row[0] for row in cursor.fetchall()]
        insert_veiculos(cursor, 1000, clientes_ids)
        con.commit()

        insert_servicos(cursor)
        insert_produtos(cursor)
        insert_funcionarios(cursor)
        con.commit()

    cursor.close()
    con.close()

if __name__ == "__main__":
    main()
