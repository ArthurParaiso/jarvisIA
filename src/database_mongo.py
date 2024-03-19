# src/database_mongo.py

from pymongo import MongoClient

# Conectando ao MongoDB local
client = MongoClient('localhost', 27017)

db = client.jarves
perg_collection = db.perg


def inserir_pergunta_e_resposta(pergunta, resposta):
    """Insere uma pergunta e resposta no MongoDB."""
    perg_collection.insert_one({
        "pergunta": pergunta,
        "resposta": resposta
    })


def pergunta_existe(pergunta):
    """Verifica se a pergunta já existe no MongoDB e retorna a resposta."""
    documento = perg_collection.find_one({"pergunta": pergunta})
    if documento:
        return documento["resposta"]
    return None
