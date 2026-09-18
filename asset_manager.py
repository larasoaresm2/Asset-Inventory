#Cadastro de tipos de ativos (imutáveis) 

#Do módulo enum, traga a ferramenta Enum
from enum import Enum 
#Crie um tipo chamado AssetType, que é uma enumeração com os valores fixos
class AssetType(Enum):  
#Cada linha liga um nome a um valor inteiro
    NOTEBOOK = 1  
    SERVER = 2  
    ROUTER = 3  
    WEB_APPLICATION = 4  
    DATABASE = 5
#Crie uma tupla que contém os níveis de severidade
SEVERITIES = ('low', 'medium', 'high', 'critical')
#Crie uma tupla, que contém os status possíveis
STATUSES = ('open', 'in_progress', 'fixed', 'risk_accepted')
#Crie um dicionário chamado assets, que será usado para armazenar os ativos
assets = {}


#Leitura com tratamento de erros

#Defina uma função que recebe uma mensagem para exibir
def read_text(message):
#Enquanto o usuário não digitar um valor válido, continue pedindo a entrada
    while True:
        text = input(message).strip()  # Remove espaços em branco no início e no final
        if text == "":  # Verifica se o texto está vazio
            print("Error: this field cannot be empty. Please enter a valid value.")
        elif ";" in text:  # Verifica se o texto contém ponto e vírgula
            print("Error: the character ';' is not allowed.")
        else: 
            return text  # Retorna o texto válido e encerra o loop
#Laço para ler um número inteiro com tratamento de erros
def read_int(message):
    while True:
        try:
            return int(input(message))  # Tenta converter a entrada para inteiro
        except ValueError:  # Captura o erro de conversão
            print(" Error: please type an integer number.")


