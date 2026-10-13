from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, DateTime, insert, text
from datetime import datetime
import re

import time
from functools import wraps
def medir_tempo(func):
    """Decorator que mede o tempo de execução de uma função."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()  # tempo inicial (mais preciso que time.time)
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()     # tempo final
        duracao = fim - inicio
        print(f"⏱ Função '{func.__name__}' executada em {duracao:.6f} segundos.")
        return resultado
    return wrapper

engine = create_engine("postgresql+psycopg2://alunos:AlunoFatec@200.19.224.150:5432/atividade2", echo=False)
metadata = MetaData()

usuarios = Table(
    'usuarios', metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(50), nullable=False, index=True),
    Column('cpf', String(14), nullable=False),
    Column('email', String(100), nullable=False, unique=True),
    Column('telefone', String(20), nullable=False),
    Column('data_nascimento', Date, nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

metadata.create_all(engine)
# anonimizar os dados
def anonimizar_nome(nome):
    part = nome.split()
    # Esse if é para caso o nome da pessoa começar com Sr., Sra., Dr. ou Dra.
    if part[0].endswith(".") and len(part) > 1:
        posicao = 1
    else:
        posicao = 0

    first_word = part[posicao]
    length = len(first_word) - 1
    first_letter = re.search(r"^(\w)", first_word).group(1)
    asterisks = "*" * length
    masked_words = first_letter + asterisks
    part[posicao] = masked_words
    return " ".join(part)

def anonimizar_cpf(cpf):
    first_numbers = cpf[:4]
    rest = cpf[4:]
    masked_numbers = re.sub(r"\d","*",rest)
    anonymate_cpf = first_numbers + masked_numbers
    return anonymate_cpf

def anonimizar_email(email):
    email_part = email.split("@")
    user = email_part[0]
    domain = email_part[1]
    length = len(user) - 1
    email_asterisks = "*" * length
    first_email_letter = user[0]
    masked_email = first_email_letter + email_asterisks + "@" + domain
    return masked_email

def anonimizar_telefone(telefone):
    digitos = re.sub(r"\D","", telefone)
    return digitos[-4:]


def LGPD(row):
    id_, nome, cpf, email, telefone, data_nascimento, created_on, updated_on = row
    nome = anonimizar_nome(nome)
    cpf = anonimizar_cpf(cpf)
    email = anonimizar_email(email)
    telefone = anonimizar_telefone(telefone)
    return (id_, nome, cpf, email, telefone, data_nascimento, created_on, updated_on)

users = []
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM usuarios LIMIT 100;"))
    for row in result:
        row = LGPD(row)
        users.append(row)

for user in users:
    print(user)