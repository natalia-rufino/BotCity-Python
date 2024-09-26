import pandas as pd
from botcity.core import DesktopBot
import time

# Defina as constantes do seu projeto
FORM_URL = "https://forms.gle/RsScG4dLXhQwADbbA"
EXCEL_FILE = "funcionarios.xlsx"

class AutomacaoCadastro(DesktopBot):
    def start(self):
        # Carregar dados do Excel
        dados = pd.read_excel(EXCEL_FILE)
        
        for index, funcionario in dados.iterrows():
            self.preencher_formulario(funcionario)
            self.atualizar_status(index)
            time.sleep(2)  # Aguarda 2 segundos entre os cadastros

    def preencher_formulario(self, funcionario):
        self.browse(FORM_URL)  # Acessa o Google Forms
        
        # Preencher o formulário
        self.find('img\campo_nome.png').click()  # Substitua com a imagem do campo de Nome
        self.type(funcionario['Nome'])
        
        self.find('img\campo_genero.png').click()  # Substitua com a imagem do campo de Gênero
        self.find('img\campo_masc.png' if funcionario['Gênero'] == 'Masculino' else 'img\campo_fem.png').click()  # Substitua com a imagem dos botões
        
        self.find('img\campo_email.png').click()  # Substitua com a imagem do campo de E-mail
        self.type(funcionario['E-mail'])
        
        self.find('img\campo_dep.png').click()  # Substitua com a imagem do campo de Departamento
        self.type(funcionario['Departamento'])
        
        self.find('img\campo_endereco.png').click()  # Substitua com a imagem do campo de Endereço
        self.type(funcionario['Endereço'])
        
        self.find('img\campo_cpf.png').click()  # Substitua com a imagem do campo de CPF
        self.type(funcionario['CPF'])
        
        self.find('img\campo_rg.png').click()  # Substitua com a imagem do campo de RG
        self.type(funcionario['RG'])
        
        self.find('img\campo_turno.png').click()  # Campo de Turno
        # Seleciona o turno com base no valor do funcionário
        if funcionario['Turno'] == 'Primeiro':
            self.find('img\campo_tur_1.png').click()  # Seleciona Primeiro
        elif funcionario['Turno'] == 'Segundo':
            self.find('img\campo_tur_2.png').click()  # Seleciona Segundo
        elif funcionario['Turno'] == 'Comercial':
            self.find('img\campo_tur_comercial.png').click()  # Seleciona Comercial
        
        #self.find('submit_button_image.png').click()  # Substitua com a imagem do botão de envio
        
    def atualizar_status(self, index):
        # Atualiza o status no Excel
        dados = pd.read_excel(EXCEL_FILE)
        dados.at[index, 'Status'] = 'Cadastrado'
        dados.to_excel(EXCEL_FILE, index=False)
        
if __name__ == "__main__":
    automacao = AutomacaoCadastro()
    automacao.start()
