import json
import os

from asset_inventory.dependency import dependency_from_dict
from asset_inventory.equipment import equipment_from_dict
from asset_inventory.vulnerability import vulnerability_from_dict


class JsonStorage:
    """Saves and loads the inventory as JSON files, each one an array of objects."""

    def __init__(self, folder="data"):
        self.folder = folder
        self.equipments_file = os.path.join(folder, "equipments.json")
        self.vulnerabilities_file = os.path.join(folder, "vulnerabilities.json")
        self.dependencies_file = os.path.join(folder, "dependencies.json")

    def save(self, inventory):
        """Write the three files with the current state of the inventory."""
        os.makedirs(self.folder, exist_ok=True)
        equipments = [equipment.to_dict() for equipment in inventory.list_equipments()]
        vulnerabilities = [v.to_dict() for v in inventory.list_vulnerabilities()]
        dependencies = [dependency.to_dict() for dependency in inventory.list_dependencies()]
        self._write(self.equipments_file, equipments)
        self._write(self.vulnerabilities_file, vulnerabilities)
        self._write(self.dependencies_file, dependencies)

    def load(self, inventory):
        """Rebuild every object and pass it through the Inventory rules.

        Order matters: vulnerabilities first (so the links can be checked),
        then equipments and their links, then the dependencies between them.
        """
        for data in self._read(self.vulnerabilities_file):
            inventory.add_vulnerability(vulnerability_from_dict(data))
        for data in self._read(self.equipments_file):
            inventory.add_equipment(equipment_from_dict(data))
            for vulnerability_id in data["vulnerability_ids"]:
                inventory.link(data["id"], vulnerability_id)
        for data in self._read(self.dependencies_file):
            inventory.add_dependency(dependency_from_dict(data))

    def _read(self, path):
        """Return the list stored in a file, or an empty list if it does not exist yet."""
        if not os.path.exists(path):
            return []
        with open(path, encoding="utf-8") as file:
            return json.load(file)

    def _write(self, path, items):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(items, file, indent=2, ensure_ascii=False)