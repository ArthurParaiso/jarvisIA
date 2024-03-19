import requests


def buscar_piada():
    url = "https://v2.jokeapi.dev/joke/Any?lang=pt"
    response = requests.get(url)

    if response.status_code != 200:
        return "Desculpe, não consegui encontrar uma piada no momento."

    data = response.json()

    if "joke" in data:
        return data["joke"]
    elif "setup" in data and "delivery" in data:
        return data["setup"] + " ... " + data["delivery"]
