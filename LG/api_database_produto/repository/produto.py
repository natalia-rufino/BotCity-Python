import database
from cotacao import obter_cotacao_dolar  # Importa a função do arquivo cotacao.py

# Inseri um novo produto 
def inserir_produto():
    # Obtém a conexão com o banco de dados
    conexao = database.criar_db()
    
    # Verifica se a conexão foi estabelecida corretamente
    if conexao:
        try:
            cursor = conexao.cursor()
            
            # Produtos a serem inseridos
            produtos = [
                ('Acai', 'Litro', 10, 12.50, 0.0),
                ('Tucuma', 'Kg', 30, 17.30, 0.0),
                ('Tapioca', 'Unid', 5, 4.70, 0.0)
            ]
            
            # Query de inserção
            query = "INSERT INTO produto (descricao, unidade, quantidade, preco_real, preco_dolar) VALUES (%s, %s, %s, %s, %s)"
            
            # Executa a query para vários produtos
            cursor.executemany(query, produtos)
            
            # Confirma a transação
            conexao.commit()

            # Retorna o último ID inserido (opcional)
            print(f"Último produto inserido com ID: {cursor.lastrowid}")
        
        except Exception as e:
            print(f"Erro ao inserir produto: {e}")
        finally:
            # Fecha o cursor e a conexão
            cursor.close()
            conexao.close()
    else:
        print("Conexão ao banco de dados falhou.")

# Chama a função de inserção
inserir_produto()

# Função para atualizar o preço dos produtos com base na cotação do dólar
def atualizar_preco_dolar():
    cotacao_dolar = obter_cotacao_dolar()

    if cotacao_dolar:
        conexao = database.criar_db()
        
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("SELECT id, descricao, preco_real FROM produto")
                produtos = cursor.fetchall()

                for produto in produtos:
                    id_produto = produto[0]
                    preco_real = produto[2]
                    preco_dolar = preco_real * cotacao_dolar

                    update_query = "UPDATE produto SET preco_dolar = %s WHERE id = %s"
                    cursor.execute(update_query, (preco_dolar, id_produto))

                conexao.commit()
                print("Preços atualizados com sucesso.")
            
            except Exception as e:
                print(f"Erro ao atualizar preço em dólar: {e}")
            finally:
                cursor.close()
                conexao.close()
        else:
            print("Conexão ao banco de dados falhou.")

# Chama as funções
if __name__ == "__main__":
    inserir_produto()  # Insere produtos primeiro
    atualizar_preco_dolar()  # Depois atualiza os preços
