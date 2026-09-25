
from assets import create_asset, read_asset, update_asset, delete_asset, list_assets
from database import load_data, save_data
from helpers import ask_yes_no
from vulnerabilities import (
    add_vulnerability,
    create_vulnerability,
    list_vulnerabilities,
    update_vulnerability_status,
)

def main():
    load_data() 

    while True:
        print("\n===== IT ASSET MANAGER =====")
        print("1 - Create asset")
        print("2 - Read asset")
        print("3 - Update asset")
        print("4 - Delete asset")
        print("5 - Add vulnerability to asset")
        print("6 - List vulnerabilities of asset")
        print("7 - List all assets")
        print("8 - Update vulnerability status")
        print("0 - Exit")
        option = input("Choose an option: ").strip()

        if option == "1":
            asset = create_asset()
            if asset is not None:
                while ask_yes_no("Add a vulnerability now?"):
                    create_vulnerability(asset)
                save_data()
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
        elif option == "7":
            list_assets()
        elif option == "8":
            update_vulnerability_status()
        elif option == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose a valid option.") 

if __name__ == "__main__":
    main()  