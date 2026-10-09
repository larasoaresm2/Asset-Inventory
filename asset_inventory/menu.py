from asset_inventory.enums import Status
from asset_inventory.equipment import Database, Notebook, Router, Server, WebApplication
from asset_inventory.helpers import (ask_yes_no, choose_from_list, read_float, read_int, read_text)
from asset_inventory.vulnerability import Vulnerability

# The classes themselves, in order shown to the user
EQUIPMENT_TYPES = [Server, Notebook, Router, WebApplication, Database]

class Menu:
    """text interface: the only class that talks to the user (print/input)."""
    def __init__(self, inventory):
        self.inventory = inventory
        self.options = {
            "1": ("Create equipment", self.create_equipment),
            "2": ("List all equipments", self.list_equipments),
            "3": ("Show equipment", self.show_equipment),
            "4": ("Update equipment", self.update_equipment),
            "5": ("Delete equipment", self.delete_equipment),
            "6": ("Create vulnerability", self.create_vulnerability),
            "7": ("List all vulnerabilities", self.list_vulnerabilities),
            "8": ("Link vulnerability to equipment", self.link_vulnerability),
            "9": ("Unlink vulnerability from equipment", self.unlink_vulnerability),
            "10": ("List vulnerabilities of equipment", self.list_vulnerabilities_of),
            "11": ("Update vulnerability", self.update_vulnerability),
            "12": ("Delete vulnerability", self.delete_vulnerability),
        }

    def run(self):
        while True:
            print("\n==== IT ASSET MANAGER ====")
            for key, (label, _) in self.options.items():
                print(f"{key} - {label}")
            print("0 - Exit")

            choice = input("Choose an option: ").strip()
            if choice == "0":
                print("Goodbye!")
                break
            if choice not in self.options:
                print("Invalid option. Please choose a valid option.")
                continue

            _, action = self.options[choice]
            try:
                action()
            except ValueError as error:
                print(f"Error: {error}")


    # Small helpers
    def _choose_equipment_type(self):
        print("Equipment types:")
        for number, equipment_class in enumerate(EQUIPMENT_TYPES, start=1):
            print(f"{number} - {equipment_class.__name__}")
        while True:
            choice = read_int("Type: ")
            if 1 <= choice <= len(EQUIPMENT_TYPES):
                return EQUIPMENT_TYPES[choice - 1]
            print("Error: option out of range.")

    def _ask_equipment(self):
        """Ask for an ID or name and return the equipment."""
        key = read_text(" Equipment ID or name: ")
        if key.isdigit():
            key = int(key)
        equipment = self.inventory.get_equipment(key)
        if equipment is None:
            raise ValueError("Equipment not found.")
        return equipment

    def _ask_until_valid(self, read_function, message, check_function):
        """Read a value and keep asking while check_function rejects it."""
        while True:
            value = read_function(message)
            try:
                check_function(value)
                return value
            except ValueError as error:
                print(f"  Error: {error}")

    def _read_cvss(self, message):
        """Keep asking until the user types a CVSS between 0.0 and 10.0."""
        while True:
            cvss = read_float(message)
            if 0.0 <= cvss <= 10.0:
                return cvss
            print("  Error: CVSS must be between 0.0 and 10.0.")


    # Equipment
    def create_equipment(self):
        equipment_class = self._choose_equipment_type()
        equipment = equipment_class(
            self._ask_until_valid(read_int, "Equipment ID (integer): ",
                                  self.inventory.check_equipment_id_available),
            self._ask_until_valid(read_text, "Name/hostname: ",
                                  self.inventory.check_name_available),
            read_text("Owner: "),
            read_text("Department/location: "),
            read_text("Description: "),
        )
        self.inventory.add_equipment(equipment)
        print("Equipment registered successfully!")

    def list_equipments(self):
        equipments = self.inventory.list_equipments()
        if not equipments:
            print("No equipments registered.")
            return
        for equipment in equipments:
            print(equipment)

    def show_equipment(self):
        equipment = self._ask_equipment()
        print(equipment)
        print(f"Description: {equipment.description}")

    def update_equipment(self):
        equipment = self._ask_equipment()
        print(equipment)
        print("Press Enter to keep the current value.")
        for field in ["name", "owner", "location", "description"]:
            current = getattr(equipment, field)
            new_value = input(f"New {field} [{current}]: ").strip()
            if new_value != "":
                if field == "name":
                    self.inventory.check_name_available(new_value, equipment.id)
                setattr(equipment, field, new_value)
        print("Equipment updated successfully!")

    def delete_equipment(self):
        equipment = self._ask_equipment()
        print(equipment)
        if ask_yes_no("Are you sure you want to delete this equipment?"):
            self.inventory.remove_equipment(equipment.id)
            print("Equipment deleted successfully!")
        else:
            print("Deletion cancelled.")

    # Vulnerabilities
    def create_vulnerability(self):
        vulnerability = Vulnerability(
            self._ask_until_valid(read_int, "Vulnerability ID (integer): ",
                                  self.inventory.check_vulnerability_id_available),
            read_text("Description: "),
            read_text("Category (e.g. weak password, outdated software): "),
            self._read_cvss("CVSS score (0.0 to 10.0): "),
            choose_from_list("Status:", Status),
        )
        self.inventory.add_vulnerability(vulnerability)
        print("Vulnerability registered successfully!")

    def list_vulnerabilities(self):
        vulnerabilities = self.inventory.list_vulnerabilities()
        if not vulnerabilities:
            print("No vulnerabilities registered.")
            return
        for vulnerability in vulnerabilities:
            print(vulnerability)

    def link_vulnerability(self):
        equipment = self._ask_equipment()
        vulnerability_id = read_int("Vulnerability ID: ")
        self.inventory.link(equipment.id, vulnerability_id)
        print(f"Vulnerability {vulnerability_id} linked to '{equipment.name}'.")

    def unlink_vulnerability(self):
        equipment = self._ask_equipment()
        vulnerability_id = read_int("Vulnerability ID: ")
        self.inventory.unlink(equipment.id, vulnerability_id)
        print(f"Vulnerability {vulnerability_id} unlinked from '{equipment.name}'.")

    def list_vulnerabilities_of(self):
        equipment = self._ask_equipment()
        vulnerabilities = self.inventory.vulnerabilities_of(equipment.id)
        if not vulnerabilities:
            print(f"'{equipment.name}' has no vulnerabilities.")
            return
        print(f"Vulnerabilities of '{equipment.name}':")
        for vulnerability in vulnerabilities:
            print(f"  {vulnerability}")

    def _ask_vulnerability(self):
        """Ask for a vulnerability ID and return it (raises if not found)."""
        vulnerability_id = read_int("Vulnerability ID: ")
        vulnerability = self.inventory.get_vulnerability(vulnerability_id)
        if vulnerability is None:
            raise ValueError("Vulnerability not found.")
        return vulnerability

    def update_vulnerability(self):
        vulnerability = self._ask_vulnerability()
        print(vulnerability)
        print("Press Enter to keep the current value.")
        new_cvss = input(f"New CVSS [{vulnerability.cvss}]: ").strip()
        if new_cvss != "":
            try:
                cvss = float(new_cvss)
            except ValueError:
                raise ValueError("CVSS must be a number.")
            vulnerability.set_cvss(cvss)
        for field in ["description", "category"]:
            current = getattr(vulnerability, field)
            new_value = input(f"New {field} [{current}]: ").strip()
            if new_value != "":
                setattr(vulnerability, field, new_value)
        if ask_yes_no("Change the status?"):
            vulnerability.status = choose_from_list("New status:", Status)
        print("Vulnerability updated successfully!")

    def delete_vulnerability(self):
        vulnerability = self._ask_vulnerability()
        print(vulnerability)
        if ask_yes_no("Delete it? It will also be unlinked from every equipment"):
            self.inventory.remove_vulnerability(vulnerability.id)
            print("Vulnerability deleted successfully!")
        else:
            print("Deletion cancelled.")