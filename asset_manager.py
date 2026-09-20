#Step1: Cadastro de tipos de ativos (imutáveis) 

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


#Step2: Leitura com tratamento de erros

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


#Step4: Arquivos: load_data() e save_data()

#Defina a função load_data, que lê os dados do arquivo e os carrega no dicionário assets
ASSETS_FILE = "assets.txt"  # Nome do arquivo que contém os ativos
VULNS_FILE = "vulnerabilities.txt"  # Nome do arquivo que contém as vulnerabilidades
SEPARADOR = ";"  # Separador usado nos arquivos

def load_data():
    """Read the text file and fills the assets dictionary"""
    try: 
        with open(ASSETS_FILE, "r", encoding="utf-8") as file:  # Abre o arquivo de ativos para leitura
            for line in file:  # Itera sobre cada linha do arquivo
                line = line.strip()
                if line == "":  # Ignora linhas vazias
                    continue
                asset_id, name, owner, location, type_code, description = line.split(SEPARADOR)  # Divide a linha em partes usando o separador
                assets[int(asset_id)] = {  # Adiciona o ativo ao dicionário assets
                    "id": int(asset_id),
                    "name": name,
                    "owner": owner,
                    "location": location,
                    "type": AssetType(int(type_code)),  # Converte o código do tipo para AssetType
                    "description": description,
                    "vulnerabilities": []  # Inicializa a lista de vulnerabilidades como vazia
                }
    except FileNotFoundError:
        pass  # Se o arquivo não existir, apenas ignore o erro e continue

def save_data():
    """Rewrites the text file with the current content of the dictionary"""
    with open(ASSETS_FILE, "w", encoding="utf-8") as file:  # Abre o arquivo de ativos para escrita
        for asset in assets.values():  # Itera sobre os valores do dicionário assets
            fields = [str(asset["id"]), asset["name"], asset["owner"], asset["location"], str(asset["type"].value), asset["description"]]  # Cria uma lista com os campos do ativo
            file.write(SEPARADOR.join(fields) + "\n")  # Escreve os campos no arquivo, separados pelo separador e adiciona uma nova linha

# --- temporary test, delete before the commit ---
load_data()
print(assets)          # the asset read from the file
save_data()            # rewrites the file with the same content



#Step3: Crie o menu principal, que será exibido para o usuário

#defina a função main, que recebe infos do usuário
def main():
    load_data() 
#Enquanto o usuário não digitar um valor válido, continue pedindo a entrada
    while True:
        print("\n===== IT ASSET MANAGER =====") #pula uma linha e exibe o título do menu
        print("1 - Register Asset")
        print("0 - Exit")
#pergunte qual opção o usuário deseja escolher e remova espaços em branco
        option = input("Choose an option: ").strip()  # Remove espaços em branco
        if option == "1":
            print("Not implemented yet.")  # Becomes create_asset() in step 4
        elif option == "0":
            break  # Sai do loop e encerra o programa
        else:
            print("Invalid option. Please choose a valid option.")

if __name__ == "__main__":
    main()  # Executa a função principal se o script for executado diretamente

