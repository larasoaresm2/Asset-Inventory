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
ASSETS_FILE = "assets.txt"  # Nome do arquivo que contém os ativos
VULNS_FILE = "vulnerabilities.txt"  # Nome do arquivo que contém as vulnerabilidades
SEPARATOR = ";"  # Separador usado nos arquivos


#Step2: Leitura com tratamento de erros

#Defina uma função que recebe uma mensagem para exibir
def read_text(message):
#Enquanto o usuário não digitar um valor válido, continue pedindo a entrada
    while True:
        text = input(message).strip()  # Remove espaços em branco no início e no final
        if text == "":  # Verifica se o texto está vazio
            print("Error: this field cannot be empty. Please enter a valid value.")
        elif SEPARATOR in text:  # Verifica se o texto contém o separador
            print(f"Error: the character '{SEPARATOR}' is not allowed.")
        else: 
            return text  # Retorna o texto válido e encerra o loop
#Laço para ler um número inteiro com tratamento de erros
def read_int(message):
    while True:
        try:
            return int(input(message))  # Tenta converter a entrada para inteiro
        except ValueError:  # Captura o erro de conversão
            print(" Error: please type an integer number.")
#Mostra uma lista numerada e devolve a opção escolhida
def choose_from_list(title, options):
    print(title)
    for number, option in enumerate(options, start=1):
        print(f"  {number} - {option}")
    while True:
        choice = read_int("Choose an option: ")
        if 1 <= choice <= len(options):
            return options[choice - 1]  # Converte a escolha (1 a 4) na posição da tupla (0 a 3)
        print("  Error: option out of range.")
#Mostra os tipos de ativo do Enum e devolve o escolhido
def choose_asset_type():
    print("Asset types:")
    for asset_type in AssetType:
        print(f"  {asset_type.value} - {asset_type.name}")
    while True:
        code = read_int("Type code: ")
        try:
            return AssetType(code)
        except ValueError:  # Código que não existe no Enum
            print("  Error: invalid type code.")
#Faz uma pergunta de sim ou não e devolve True ou False
def ask_yes_no(message):
    while True:
        answer = input(message + " (y/n): ").strip().lower()
        if answer in ("y", "n"):
            return answer == "y"
        print("  Error: type 'y' or 'n'.")


#Step4: Arquivos: load_data() e save_data()

#Defina a função load_data, que lê os dados do arquivo e os carrega no dicionário assets
def load_data():
    """Read the text file and fills the assets dictionary"""
    try: 
        with open(ASSETS_FILE, "r", encoding="utf-8") as file:  # Abre o arquivo de ativos para leitura
            for line in file:  # Itera sobre cada linha do arquivo
                line = line.strip()
                if line == "":  # Ignora linhas vazias
                    continue
                asset_id, name, owner, location, type_code, description = line.split(SEPARATOR)  # Divide a linha em partes usando o separador
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
            file.write(SEPARATOR.join(fields) + "\n")  # Escreve os campos no arquivo, separados pelo separador e adiciona uma nova linha


#Step5: CRUD de ativos 


#Step6: Vulnerabilidades


#Step3: Crie o menu principal, que será exibido para o usuário

#defina a função main, que recebe infos do usuário
def main():
    load_data() 
#Enquanto o usuário não digitar um valor válido, continue pedindo a entrada
    while True:
        print("\n===== IT ASSET MANAGER =====")
        print("1 - Register asset")
        print("2 - Search asset")
        print("3 - Update asset")
        print("4 - Delete asset")
        print("5 - Add vulnerability to asset")
        print("6 - List vulnerabilities of asset")
        print("0 - Exit")
        option = input("Choose an option: ").strip()

        if option == "1":
            print("Not implemented yet.")  # Becomes create_asset() in step 5
        elif option == "2":
            print("Not implemented yet.")  # Becomes read_asset() in step 5
        elif option == "3":
            print("Not implemented yet.")  # Becomes update_asset() in step 5
        elif option == "4":
            print("Not implemented yet.")  # Becomes delete_asset() in step 5
        elif option == "5":
            print("Not implemented yet.")  # Becomes add_vulnerability() in step 6
        elif option == "6":
            print("Not implemented yet.")  # Becomes list_vulnerabilities() in step 6
        elif option == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose a valid option.")

if __name__ == "__main__":
    main()  # Executa a função principal se o script for executado diretamente

