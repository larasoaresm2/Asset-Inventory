import logging
import os

from asset_inventory.inventory import Inventory
from asset_inventory.log_config import setup_logging
from asset_inventory.menu import Menu
from asset_inventory.storage import JsonStorage

logger = logging.getLogger("main")


def main():
    setup_logging("data", os.environ.get("LOG_LEVEL", "INFO"))
    logger.info("Application started")
    inventory = Inventory()
    storage = JsonStorage("data")
    try:
        storage.load(inventory)
    except ValueError as error:
        print(f"Could not load the saved data: {error}")
        logger.error("Could not load the saved data: %s", error)
        return
    logger.info(
        "Loaded %d equipments, %d vulnerabilities and %d dependencies",
        len(inventory.list_equipments()),
        len(inventory.list_vulnerabilities()),
        len(inventory.list_dependencies()),
    )
    menu = Menu(inventory, storage)
    try:
        menu.run()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
    except Exception:
        logger.exception("Unexpected error")
        raise
    logger.info("Application stopped")


if __name__ == "__main__":
    main()
