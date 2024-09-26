import requests

def obter_cotacao_dolar():
    url = 'https://economia.awesomeapi.com.br/last/USD-BRL'
    response = requests.get(url)
    
    if response.status_code == 200:
        dados = response.json()
        # Retorna o valor mais alto ("high") da cotação do dólar
        return float(dados['USDBRL']['high'])
    else:
        print("Erro ao obter a cotação do dólar")
        return None
