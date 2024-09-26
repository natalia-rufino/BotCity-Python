from flask import Flask, make_response, jsonify
import sys
import os
import requests

# Atualizar o path do projeto para localizar os módulos da pasta repository
modulo = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'repository'))
sys.path.append(modulo)

import produto
from cotacao import obter_cotacao_dolar  # Importa a função do arquivo cotacao.py

# Instanciar 
app_api = Flask('api_database')
app_api.config['JSON_SORT_KEYS'] = False

# --------------------------------------------------------
# Serviço: Buscar cotação do dólar
# --------------------------------------------------------

@app_api.route('/dolar/cotacao', methods=['GET'])
def consultar_cotacao_dolar():
    cotacao = obter_cotacao_dolar()
    if cotacao is not None:
        return make_response(jsonify(status=True, cotacao=cotacao), 200)
    else:
        return make_response(jsonify(status=False, mensagem="Erro ao obter cotação do dólar"), 500)

# --------------------------------------------------------
# Serviço: Atualizar o preço dos produtos com a cotação do dólar
# --------------------------------------------------------

@app_api.route('/produto/atualizar_preco_dolar', methods=['PUT'])
def atualizar_preco_produtos_com_dolar():
    try:
        cotacao_dolar = obter_cotacao_dolar()  # Obter a cotação atual do dólar
        if cotacao_dolar is None:
            return make_response(
                jsonify(status=False, mensagem="Não foi possível obter a cotação do dólar"), 500)
        
        # Listar todos os produtos
        lista_produto = produto.listar_produto()  # Certifique-se de que essa função existe em produto.py
        
        if len(lista_produto) == 0:
            return make_response(
                jsonify(status=False, mensagem="Nenhum produto encontrado para atualizar"), 404)
        
        for prod in lista_produto:
            preco_real = float(prod['preco_real'])
            preco_dolar = preco_real * cotacao_dolar
            prod['preco_dolar'] = preco_dolar
            produto.atualizar_produto(prod)
        
        return make_response(
            jsonify(status=True, mensagem="Preços dos produtos atualizados com sucesso"), 200)
    
    except Exception as ex:
        return make_response(
            jsonify(status=False, mensagem=f"Erro ao atualizar preços: {ex}"), 500)

# --------------------------------------------------------
#           Inicio: Serviços da api usuário 
# --------------------------------------------------------
# (Os serviços de usuário continuam os mesmos, sem modificações)
# --------------------------------------------------------

# --------------------------------------------------------
#           Inicio: Serviços da api produto 
# --------------------------------------------------------
# (Os serviços de produto como criar, atualizar, deletar continuam os mesmos)
# --------------------------------------------------------

# Levantar/Executar API REST: api_database
#if __name__ == '__main__':
app_api.run()
