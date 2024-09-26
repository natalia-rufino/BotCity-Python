from botcity.core import BotCity
import requests

class BotCotacao(BotCity):

    def action(self):
        # URL da sua API Flask
        url_cotacao = "http://localhost:5000/dolar/cotacao"  # Ajuste a URL conforme necessário

        # Fazendo uma requisição GET para obter a cotação
        response = requests.get(url_cotacao)

        if response.status_code == 200:
            dados = response.json()
            if dados['status']:
                cotacao = dados['cotacao']
                print(f"Cotação do dólar: {cotacao}")
            else:
                print(f"Erro: {dados['mensagem']}")
        else:
            print(f"Erro ao chamar a API: {response.status_code}")

        # Aqui você pode adicionar mais lógica para interagir com outros endpoints da sua API
        # Exemplo: Atualizar preços de produtos
        url_atualizar_preco = "http://localhost:5000/produto/atualizar_preco_dolar"
        response = requests.put(url_atualizar_preco)

        if response.status_code == 200:
            print("Preços dos produtos atualizados com sucesso.")
        else:
            print(f"Erro ao atualizar preços: {response.status_code}")

# Inicializa o bot
if __name__ == "__main__":
    BotCotacao().run()
