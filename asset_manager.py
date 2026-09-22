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
                line = line.strip()  #remove espaços em branco no início e no final da linha
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

    try:
        with open(VULNS_FILE, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                asset_id, description, category, severity, status = line.split(SEPARATOR)
                asset_id = int(asset_id)
                if asset_id in assets:                 # ignores orphan lines
                    assets[asset_id]["vulnerabilities"].append({
                        "description": description,
                        "category": category,
                        "severity": severity,
                        "status": status,
                    })
    except FileNotFoundError:
        pass


def save_data():
    """Rewrites the text file with the current content of the dictionary"""
    with open(ASSETS_FILE, "w", encoding="utf-8") as file:  # Abre o arquivo de ativos para escrita
        for asset in assets.values():  # Itera sobre os valores do dicionário assets
            fields = [str(asset["id"]), asset["name"], asset["owner"], asset["location"], str(asset["type"].value), asset["description"]]  # Cria uma lista com os campos do ativo
            file.write(SEPARATOR.join(fields) + "\n")  # Escreve os campos no arquivo, separados pelo separador e adiciona uma nova linha

    with open(VULNS_FILE, "w", encoding="utf-8") as file:
        for asset in assets.values():
            for vuln in asset["vulnerabilities"]:
                fields = [str(asset["id"]), vuln["description"], vuln["category"],
                          vuln["severity"], vuln["status"]]
                file.write(SEPARATOR.join(fields) + "\n")


#Step5: CRUD de ativos 
#Crie as funções de buscar e exibir
def find_asset():
    """Asks for an ID or a name and returns the asset (or none)."""
    key = read_text("Type the asset ID or name: ")
    if key.isdigit():
        return assets.get(int(key))
    for asset in assets.values():
        if asset["name"].lower() == key.lower():
            return asset
    return None
def show_asset(asset):
    """Prints one asset in an organized way."""
    print("-" * 40)
    print(f"ID: {asset['id']}")
    print(f"Name: {asset['name']}")
    print(f"Owner: {asset['owner']}")
    print(f"Location: {asset['location']}")
    print(f"Type: {asset['type'].name}   (code {asset['type'].value})")
    print(f"Description: {asset['description']}")
    print("-"*40)

#Crie uma função para cadastrar um ativo
def create_asset():
    asset_id = read_int("Asset ID (integer): ")
    if asset_id in assets:                    # unique id (requirement 3)
        print("Error: this ID already exists.")
        return

    assets[asset_id] = {
        "id": asset_id,
        "name": read_text("Name/hostname: "),
        "owner": read_text("Owner: "),
        "location": read_text("Department/location: "),
        "type": choose_asset_type(),
        "description": read_text("Description: "),
        "vulnerabilities": [],
    }
    while ask_yes_no("Add a vulnerability now?"):
        create_vulnerability(assets[asset_id])
    save_data()
    print("Asset registered successfully!")

#Crie uma função para consultar um ativo
def read_asset():
    asset = find_asset()
    if asset is None:
        print("Asset not found.")
    else:
        show_asset(asset)

#crie uma função para atualizar um ativo
def update_asset():
    asset = find_asset()
    if asset is None:
        print("Asset not found.")
        return

    show_asset(asset)
    print("Type the new value or press Enter to keep the current one.")
    for field in ["name", "owner", "location", "description"]:
        new_value = input(f"New {field} [{asset[field]}]: ").strip()
        if SEPARATOR in new_value:
            print(f"  Ignored: the character '{SEPARATOR}' is not allowed.")
        elif new_value != "":
            asset[field] = new_value

    if ask_yes_no("Change the asset type?"):
        asset["type"] = choose_asset_type()

    save_data()
    print("Asset updated.")

#Crie uma função para deletar um ativo
def delete_asset():
    asset = find_asset()
    if asset is None:
        print("Asset not found.")
        return

    show_asset(asset)
    if ask_yes_no("Are you sure you want to delete this asset?"):
        del assets[asset["id"]]     # its vulnerabilities go away together
        save_data()
        print("Asset and its vulnerabilities deleted.")


#Step6: Vulnerabilidades
#Cadastrar uma vulnerabilidade
def create_vulnerability(asset):
    """Registers one vulnerability for an asset already found."""
    vuln = {
        "description": read_text("Vulnerability description: "),
        "category": read_text("Category (e.g. weak password, outdated software): "),
        "severity": choose_from_list("Severity:", SEVERITIES),
        "status": choose_from_list("Status:", STATUSES),
    }
    asset["vulnerabilities"].append(vuln)
    print("Vulnerability added.")


def add_vulnerability():
    """Menu option: finds the asset and adds a vulnerability to it."""
    asset = find_asset()
    if asset is None:
        print("Asset not found.")
        return
    create_vulnerability(asset)
    save_data()

#liste as vulnerabilidades de um ativo
def list_vulnerabilities():
    asset = find_asset()
    if asset is None:
        print("Asset not found.")
        return

    if len(asset["vulnerabilities"]) == 0:
        print(f"The asset '{asset['name']}' has no registered vulnerabilities.")
        return

    print(f"Vulnerabilities of '{asset['name']}':")
    for number, vuln in enumerate(asset["vulnerabilities"], start=1):
        print(f"  {number}. {vuln['description']} | category: {vuln['category']} "
              f"| severity: {vuln['severity']} | status: {vuln['status']}")




#Step3: Crie o menu principal, que será exibido para o usuário
#defina a função main, que recebe infos do usuário
def main():
    load_data() 
#Enquanto o usuário não digitar um valor válido, continue pedindo a entrada
    while True:
        print("\n===== IT ASSET MANAGER =====")
        print("1 - Create asset")
        print("2 - Read asset")
        print("3 - Update asset")
        print("4 - Delete asset")
        print("5 - Add vulnerability to asset")
        print("6 - List vulnerabilities of asset")
        print("0 - Exit")
        option = input("Choose an option: ").strip()

        if option == "1":
            create_asset()
        elif option == "2":
            read_asset()
        elif option == "3":
            update_asset()
        elif option == "4":
            delete_asset()
        elif option == "5":
            add_vulnerability()
        elif option == "6":
            list_vulnerabilities()
        elif option == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose a valid option.") 

if __name__ == "__main__":
    main()  # Executa a função principal se o script for executado diretamente