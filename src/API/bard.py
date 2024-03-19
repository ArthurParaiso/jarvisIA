from bardapi import Bard


def consultar_bard(pergunta, continuar_conversa=False):
    try:
        # Inicializa Bard.
        bard = Bard(token_from_browser=True)

        # Faz a pergunta e obtém a resposta.
        resposta = bard.get_answer(pergunta)['content']

        # Se continuar_conversa estiver habilitado, faz a segunda pergunta.
        if continuar_conversa:
            resposta_continuada = bard.get_answer("What is my last prompt??")['content']
            return resposta, resposta_continuada

        return resposta

    except Exception as e:
        print(f"Erro ao consultar Bard: {e}")
        return None
