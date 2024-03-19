import argparse
import os

from src.API.bard import consultar_bard
from src.API.currency_layer import processo_conversao
from src.API.joke import buscar_piada
from src.database import obter_resposta_padrao
from src.database_mongo import pergunta_existe, inserir_pergunta_e_resposta

os.environ['_BARD_API_KEY'] = 'awh8UixGmZ5ZQZxxsGCIX7XIhmS9gF_tNxlEf4m_E3GvLEvBCLKzPt4Ozs0gRqjf4LjREQ.'


def responder_pergunta(pergunta):
    """
    Responde à pergunta do usuário com base em palavras-chave ou consultando bancos de dados.
    """
    lower_pergunta = pergunta.lower()

    if "converter" in lower_pergunta or "taxa de câmbio" in lower_pergunta:
        return processo_conversao()

    if "piada" in lower_pergunta or "conte uma piada" in lower_pergunta:
        return "Jarves: " + buscar_piada()

    if pergunta in ["sair", "tchau", "bye"]:
        return "Jarves: Até logo!"

    resposta = pergunta_existe(pergunta)
    if not resposta:
        resposta = obter_resposta_padrao(pergunta)

    if resposta:
        return f"Jarves: {resposta}"
    else:
        resposta_bard = consultar_bard(pergunta)
        if resposta_bard:
            return f"Jarves (via Bard): {resposta_bard}"
        else:
            print("Jarves: Desculpe, não conheço a resposta. Poderia me explicar?")
            resposta_usuario = input("Você: ")
            inserir_pergunta_e_resposta(pergunta, resposta_usuario)
            return "Jarves: Obrigado por me explicar! Agora sei a resposta."


def main():
    """Inicie o IA."""
    parser = argparse.ArgumentParser(description="Inteligencia Artificial - Jarves")
    parser.add_argument("pergunta", type=str, nargs="?", help="Faça uma pergunta à IA")

    args = parser.parse_args()
    pergunta = args.pergunta

    if pergunta:
        print(responder_pergunta(pergunta))
    else:
        print("Jarves: Olá! Como posso ajudar você hoje?")
        while True:
            pergunta = input("Você: ")
            resposta = responder_pergunta(pergunta)
            print(resposta)

            if "Até logo!" in resposta:
                break


if __name__ == "__main__":
    main()
