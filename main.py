from asset_inventory.inventory import Inventory
from asset_inventory.menu import Menu

def main():
    menu = Menu(Inventory())
    menu.run()

if __name__ == "__main__":
    main()