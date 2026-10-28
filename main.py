from asset_inventory.inventory import Inventory
from asset_inventory.menu import Menu
from asset_inventory.storage import JsonStorage


def main():
    inventory = Inventory()
    storage = JsonStorage("data")
    try:
        storage.load(inventory)
    except ValueError as error:
        print(f"Could not load the saved data: {error}")
        return
    menu = Menu(inventory, storage)
    try:
        menu.run()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
