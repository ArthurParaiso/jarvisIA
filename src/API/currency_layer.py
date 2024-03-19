import requests

CURRENCYLAYER_ENDPOINT = "http://apilayer.net/api/live"
API_KEY = "87daceba3b644d6ecd820795a0b21834"


def obter_taxa_cambio(moeda_origem, moeda_destino):
    parametros = {
        'access_key': API_KEY,
        'currencies': f"{moeda_origem},{moeda_destino}",
        'format': 1
    }

    try:
        response = requests.get(CURRENCYLAYER_ENDPOINT, params=parametros)
        data = response.json()
        if response.status_code != 200 or "error" in data:
            return None
        taxa_origem = data['quotes'][f"USD{moeda_origem}"]
        taxa_destino = data['quotes'][f"USD{moeda_destino}"]
        taxa_cambio = taxa_destino / taxa_origem

        return taxa_cambio

    except Exception as e:
        print(f"Erro ao consultar a CurrencyLayer: {e}")
        return None


def converter_valor(moeda_origem, moeda_destino, valor):
    try:
        taxa_cambio = obter_taxa_cambio(moeda_origem, moeda_destino)
        return valor * taxa_cambio
    except Exception as e:
        print(f"Jarves: Erro ao converter, tente novamente ")
        return None


def escolher_moedas():
    print("Jarves: Selecione a moeda de origem:")
    print("1. Dólar (USD)")
    print("2. Real (BRL)")
    print("3. Euro (EUR)")

    moeda_origem = input("Digite o número da moeda de origem: ")

    print("\nJarves: Selecione a moeda de destino:")
    print("1. Dólar (USD)")
    print("2. Real (BRL)")
    print("3. Euro (EUR)")

    moeda_destino = input("Digite o número da moeda de destino: ")

    mapping = {
        "1": "USD",
        "2": "BRL",
        "3": "EUR"
    }

    return mapping.get(moeda_origem, "USD"), mapping.get(moeda_destino, "USD")


def validar_valor_numerico(valor):
    try:
        valor_float = float(valor)
        return True, valor_float
    except ValueError:
        return False, None


def validar_moeda(moeda):
    moedas_validas = ["USD", "BRL", "EUR"]
    if moeda in moedas_validas:
        return True
    else:
        return False


def processo_conversao():
    moeda_origem, moeda_destino = escolher_moedas()
    try:
        valor = float(input("Jarves: Qual valor você deseja converter? (Ex: 100): "))
    except ValueError:
        return "Jarves: Você não inseriu um valor válido."

    valor_convertido = converter_valor(moeda_origem, moeda_destino, valor)

    if valor_convertido is not None:
        return f"Jarves: {valor} {moeda_origem} é igual a {valor_convertido:.2f} {moeda_destino}."
    else:
        return "Jarves: Desculpe, não pude converter o valor neste momento. Verifique as moedas ou tente novamente mais tarde."
