from asset_inventory.inventory import Inventory
from asset_inventory.menu import Menu

def main():
    menu = Menu(Inventory())
    try:
        menu.run()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")

if __name__ == "__main__":
    main()