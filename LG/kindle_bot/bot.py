# Import para automação web
from botcity.web import WebBot, Browser, By

# Import para integração com o BotCity Maestro SDK
from botcity.maestro import *

from webdriver_manager.chrome import ChromeDriverManager

# Biblioteca para fazer requisições HTTP
import requests

# Desabilitar erros caso não estejamos conectados ao Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

# Função para converter o valor de dólar para real usando a API da AwesomeAPI
def converter_dolar_para_real(valor_em_dolar):
    url = 'https://economia.awesomeapi.com.br/json/last/USD-BRL'
    response = requests.get(url)
    dados = response.json()
    cotacao_dolar = float(dados['USDBRL']['bid'])
    valor_em_real = valor_em_dolar * cotacao_dolar
    return valor_em_real

# Função principal do bot
def main():
    # Inicializa o WebBot
    bot = WebBot()

    # Configura para rodar com a interface gráfica (não em modo headless)
    bot.headless = False

    bot.browser = Browser.CHROME

    # Uncomment to set the WebDriver path
    bot.driver_path = ChromeDriverManager().install()

    # Abre o site da Amazon
    bot.browse("https://www.amazon.com")

    # Aguarda a página carregar e localiza o campo de pesquisa
    bot.wait(5000)

    
# Identifica o nome e o preço do produto Kindle
    try:
        # Localiza o campo de pesquisa e insere "kindle"
        print("Tentando encontrar o campo de pesquisa...")
        search_box = bot.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]')
        search_box.click()
        search_box.send_keys("kindle")
        print("Texto 'kindle' inserido no campo de pesquisa.")
        
        # Clica no botão de pesquisa
        print("Tentando encontrar o botão de pesquisa...")
        search_button = bot.find_element(By.XPATH, '//*[@id="nav-search-submit-button"]')
        search_button.click()
        print("Botão de pesquisa clicado.")
        
        # Aguarda a página de resultados carregar
        bot.wait(5000)  # Aguarda 5 segundos para os resultados carregarem

        # Tenta encontrar o preço do primeiro produto
        print("Tentando encontrar o preço do produto...")
        preco_whole = bot.find_element(By.XPATH, '//*[@class="a-price-whole"]')
        preco_decimal = bot.find_element(By.XPATH, '//*[@class="a-price-decimal"]')
        
        preco_em_dolar = preco_whole.text + preco_decimal.text
        preco_em_dolar = float(preco_em_dolar.replace(',', '').replace('.', '.'))

        # Converte e exibe o preço
        preco_em_real = converter_dolar_para_real(preco_em_dolar)
        print(f"Nome do Produto: Kindle")
        print(f"Valor em Dólar: ${preco_em_dolar:.2f}")
        print(f"Valor em Real: R${preco_em_real:.2f}")

    except Exception as e:
        print(f"Erro: {e}")
        # Finaliza o navegador
    
    bot.stop_browser()

# Executa o bot
if __name__ == '__main__':
    main()