from constants import SEPARATOR
from enums import AssetType


def read_text(message):

    while True:
        text = input(message).strip()  
        if text == "": 
            print("Error: this field cannot be empty. Please enter a valid value.")
        elif SEPARATOR in text: 
            print(f"Error: the character '{SEPARATOR}' is not allowed.")
        else: 
            return text  

def read_int(message):
    while True:
        try:
            return int(input(message))  
        except ValueError:  
            print(" Error: please type an integer number.")

def choose_from_list(title, options):
    members = list(options)
    print(title)
    for number, option in enumerate(members, start=1):
        print(f"  {number} - {option.name}")
    while True:
        choice = read_int("Choose an option: ")
        if 1 <= choice <= len(members):
            return members[choice - 1]
        print("  Error: option out of range.")

def choose_asset_type():
    print("Asset types:")
    for asset_type in AssetType:
        print(f"  {asset_type.value} - {asset_type.name}")
    while True:
        code = read_int("Type code: ")
        try:
            return AssetType(code)
        except ValueError:  
            print("  Error: invalid type code.")

def ask_yes_no(message):
    while True:
        answer = input(message + " (y/n): ").strip().lower()
        if answer in ("y", "n"):
            return answer == "y"
        print("  Error: type 'y' or 'n'.")