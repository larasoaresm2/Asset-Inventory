from constants import SEPARATOR
from database import assets, save_data
from helpers import ask_yes_no, choose_asset_type, read_int, read_text


def find_asset():
    """Asks for an ID or a name and returns the asset (or None)."""
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
    print(f"Type: {asset['type'].name}")
    print(f"Description: {asset['description']}")
    print("-"*40)


def list_assets():
    """Prints every registered asset."""
    if len(assets) == 0:
        print("No assets registered.")
        return
    for asset in assets.values():
        show_asset(asset)


def create_asset():
    asset_id = read_int("Asset ID (integer): ")
    if asset_id in assets:                    
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
    save_data()
    print("Asset registered successfully!")
    return assets[asset_id]


def read_asset():
    if not assets:
        print("No assets registered.")
        return
    asset = find_asset()
    if asset is None:
        print("Asset not found.")
    else:
        show_asset(asset)


def update_asset():
    if not assets:
        print("No assets registered.")
        return
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


def delete_asset():
    if not assets:
        print("No assets registered.")
        return
    asset = find_asset()
    if asset is None:
        print("Asset not found.")
        return

    show_asset(asset)
    if ask_yes_no("Are you sure you want to delete this asset?"):
        del assets[asset["id"]]     # its vulnerabilities go away together
        save_data()
        print("Asset and its vulnerabilities deleted.")