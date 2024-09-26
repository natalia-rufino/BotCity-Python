# Importações necessárias
import pandas as pd
import time
import logging
import os
from dotenv import load_dotenv
from time import sleep

from webdriver_manager.chrome import ChromeDriverManager

from botcity.core import DesktopBot
#from botcity.plugins.http import BotHttpPlugin

# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Import for integration with BotCity Maestro SDK
from botcity.maestro import BotMaestroSDK, AutomationTaskFinishStatus

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

# Configuração de logs
logging.basicConfig(
    filename='automacao.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# class Bot(DesktopBot):
#     def action(self, execution=None):
#         # Inicializa o plugin HTTP
#         http_plugin = BotHttpPlugin()

def preencher_formulario(bot, dados):
    """
    Preenche o formulário Google Forms com os dados fornecidos.

    Args:
        bot (WebBot): Instância do BotCity WebBot.
        dados (dict): Dicionário com os dados do funcionário.
    
    Returns:
        bool: True se o formulário foi submetido com sucesso, False caso contrário.
    """
    try:
        # URL do Google Forms
        form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfDzqYUoNJMY09vo4o9NNmwWWzgoNHMX3on6wctH2z3rQkB1A/viewform"

        # Abrir o formulário no navegador
        bot.browse(form_url)
        logging.info(f"Abrindo formulário para {dados['Nome']}")
        time.sleep(5)  # Aguardar o carregamento do formulário

        # Preencher Nome
        nome_xpath = '//*[@id="i1"]'
        bot.find_element(By.XPATH, nome_xpath).send_keys(dados['Nome'])
        logging.info(f"Nome preenchido: {dados['Nome']}")

        # Preencher Gênero
        genero_xpath_m = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div/span/div/div[1]/label/div/div[2]/div/span'
        genero_xpath_f = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div/span/div/div[2]/label/div/div[2]/div/span'
        if dados['Gênero'].lower() == 'masculino':
            bot.find_element(By.XPATH, genero_xpath_m).click()
            logging.info(f"Gênero selecionado: Masculino")
        else:
            bot.find_element(By.XPATH, genero_xpath_f).click()
            logging.info(f"Gênero selecionado: Feminino")
        time.sleep(1)

        # Preencher E-mail
        email_xpath = '//*[@id="i15"]'
        bot.find_element(By.XPATH, email_xpath).send_keys(dados['E-mail'])
        logging.info(f"E-mail preenchido: {dados['E-mail']}")

        # Preencher Departamento
        departamento_xpath = '//*[@id="i19"]'
        bot.find_element(By.XPATH, departamento_xpath).send_keys(dados['Departamento'])
        logging.info(f"Departamento preenchido: {dados['Departamento']}")

        # Preencher Endereço
        endereco_xpath = '//*[@id="i23"]'
        bot.find_element(By.XPATH, endereco_xpath).send_keys(dados['Endereço'])
        logging.info(f"Endereço preenchido: {dados['Endereço']}")

        # Preencher CPF
        cpf_xpath = '//*[@id="i27"]'
        bot.find_element(By.XPATH, cpf_xpath).send_keys(dados['CPF'])
        logging.info(f"CPF preenchido: {dados['CPF']}")

        # Preencher RG
        rg_xpath = '//*[@id="i31"]'
        bot.find_element(By.XPATH, rg_xpath).send_keys(dados['RG'])
        logging.info(f"RG preenchido: {dados['RG']}")

        # Preencher Turno
        turno_xpath_p = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[8]/div/div/div[2]/div/div/span/div/div[1]/label/div/div[2]/div/span'
        turno_xpath_s = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[8]/div/div/div[2]/div/div/span/div/div[2]/label/div/div[2]/div/span'
        turno_xpath_c = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[8]/div/div/div[2]/div/div/span/div/div[3]/label/div/div[2]/div/span'
        if dados['Turno'].lower() == 'primeiro':
            bot.find_element(By.XPATH, turno_xpath_p).click()
            logging.info(f"Turno selecionado: Primeiro")
        elif dados['Turno'].lower() == 'segundo':
            bot.find_element(By.XPATH, turno_xpath_s).click()
            logging.info(f"Turno selecionado: Segundo")
        else:
            bot.find_element(By.XPATH, turno_xpath_c).click()
            logging.info(f"Turno selecionado: Comercial")
        time.sleep(1)

        # Submeter o formulário
        submit_xpath = '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/div[2]'
        bot.find_element(By.XPATH, submit_xpath).click()
        logging.info(f"Formulário submetido para {dados['Nome']}")
        time.sleep(3)  # Aguardar a submissão

        return True

    except Exception as e:
        logging.error(f"Erro ao preencher o formulário para {dados['Nome']}: {e}")
        return False

#Carrega as variáveis de ambiente
load_dotenv()
EMAIL = os.getenv('EMAIL')
SENHA = os.getenv('PASSWORD')

def fazer_login(bot):
    while True:
        try:
            # Acessa os campos de username e password
            login_button_xpath = '/html/body/div[2]/div/div[2]/div[3]/div[2]'
            login_button = bot.find_element(By.XPATH, login_button_xpath)
            login_button.click()
            usuario_xpath = '//*[@id="identifierId"]' 
            senha_xpath = '//*[@id="password"]/div[1]/div/div[1]/input'
            bot.find_element(By.XPATH, usuario_xpath).send_keys("natalia.rufino@ifam.edu.br")
            bot.find_element(By.XPATH, senha_xpath).send_keys("035.827.022-78")
            bot.find_element(By.XPATH, '//*[@id="passwordNext"]').click()  # Botão de login
            time.sleep(5)  # Aguardar o carregamento após o login
            break
        except Exception as e:
            logging.error(f"Erro no login: {e}")
            print("Erro no login, tentando novamente...")

def gerar_relatorio(df):
    """
    Gera um relatório do progresso do cadastro.

    Args:
        df (DataFrame): DataFrame com os dados dos funcionários.
    """
    total = len(df)
    cadastrados = len(df[df['Status'] == "Cadastrado"])
    pendentes = len(df[df['Status'] == "Pendente"])

    logging.info("------ Relatório Final ------")
    logging.info(f"Total de Funcionários: {total}")
    logging.info(f"Cadastrados: {cadastrados}")
    logging.info(f"Pendente: {pendentes}")

    # Imprimir no console
    print("Relatório de Cadastro de Funcionários")
    print("-------------------------------------")
    print(f"Total de Funcionários: {total}")
    print(f"Cadastrados: {cadastrados}")
    print(f"Pendente: {pendentes}")

def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    ## Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    #bot = CadastroBot(driver_path='/usr/bin/chromedriver')
    bot = DesktopBot()

    # Fazer login
    #fazer_login(bot)

    # Configure whether or not to run on headless mode
    bot.headless = False

    bot.driver_path = ChromeDriverManager().install()

    # Carregar dados do Excel
    excel_path = "funcionarios.xlsx"
    excel_atualizado = "funcionarios_atualizado.xlsx"

    if not os.path.exists(excel_path):
        logging.error(f"Arquivo {excel_path} não encontrado.")
        return

    df = pd.read_excel(excel_path)

    for index, row in df.iterrows():
        if row['Status'] != "Cadastrado":
            dados = {
                'Nome': row['Nome'],
                'Gênero': row['Gênero'],
                'E-mail': row['E-mail'],
                'Departamento': row['Departamento'],
                'Endereço': row['Endereço'],
                'CPF': row['CPF'],
                'RG': row['RG'],
                'Turno': row['Turno']
            }

            sucesso = preencher_formulario(bot, dados)

            if sucesso:
                # Atualizar o status no DataFrame
                df.at[index, 'Status'] = "Cadastrado"
                logging.info(f"Status atualizado para Cadastrado: {dados['Nome']}")
            else:
                logging.warning(f"Cadastro pendente para: {dados['Nome']}")

            # Salvar progresso após cada tentativa
            df.to_excel(excel_atualizado, index=False)
            logging.info(f"Progresso salvo em {excel_atualizado}")

    # Gerar relatório final
    gerar_relatorio(df)

    # Wait 3 seconds before closing
    bot.wait(5000)

    # Finish and clean up the Web Browser
    bot.stop_browser()

    # Uncomment to mark this task as finished on BotMaestro
    maestro.finish_task(
        task_id=execution.task_id,
        status=AutomationTaskFinishStatus.SUCCESS,
        message="Task Finished OK."
    )

#def not_found(label):
#   print(f"Element not found: {label}")

if __name__ == '__main__':
    main()
