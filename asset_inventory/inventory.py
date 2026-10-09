class Inventory:
    """Keeps all equipments and vulnerabilities and enforces the rules that connect them."""
    def __init__(self):
        self.equipments = {}
        self.vulnerabilities = {}

    # Equipments
    def add_equipment(self, equipment):
        self.check_equipment_id_available(equipment.id)
        self.check_name_available(equipment.name)
        self.equipments[equipment.id] = equipment

    def check_equipment_id_available(self, equipment_id):
        """IDs must be positive and not used by another equipment."""
        if equipment_id <= 0:
            raise ValueError("Equipment ID must be a positive integer.")
        if equipment_id in self.equipments:
            raise ValueError(f"Equipment with ID {equipment_id} already exists.") 

    def check_name_available(self, name, current_id=None):
        """Names must be unique (ignoring case) and not only digits,
        so that a search by name is never ambiguous or confused with an ID."""
        if name.isdigit():
            raise ValueError("Name cannot contain only digits.")
        existing = self.get_equipment(name)
        if existing is not None and existing.id != current_id:
            raise ValueError(f"An equipment named '{existing.name}' already exists.")


    def get_equipment(self, key):
        """Find an equipment by ID (int) or name (str). Returns None if not found."""
        if isinstance(key, int):
            return self.equipments.get(key)
        for equipment in self.equipments.values():
            if equipment.name.lower() == key.lower():
                return equipment
        return None

    def remove_equipment(self, equipment_id):
        if equipment_id not in self.equipments:
            raise ValueError(f"Equipment with ID {equipment_id} does not exist.")
        del self.equipments[equipment_id]

    def list_equipments(self):
        return list(self.equipments.values())

    # Vulnerabilities
    def add_vulnerability(self, vulnerability):
        self.check_vulnerability_id_available(vulnerability.id)
        self.vulnerabilities[vulnerability.id] = vulnerability

    def check_vulnerability_id_available(self, vulnerability_id):
        """IDs must be positive and not used by another vulnerability."""
        if vulnerability_id <= 0:
            raise ValueError("Vulnerability ID must be a positive integer.")
        if vulnerability_id in self.vulnerabilities:
            raise ValueError(f"Vulnerability with ID {vulnerability_id} already exists.")
        

    def get_vulnerability(self, vulnerability_id):
        return self.vulnerabilities.get(vulnerability_id)

    def remove_vulnerability(self, vulnerability_id):
        if vulnerability_id not in self.vulnerabilities:
            raise ValueError(f"Vulnerability with ID {vulnerability_id} does not exist.")
        for equipment in self.equipments.values():
            equipment.remove_vulnerability(vulnerability_id)
        del self.vulnerabilities[vulnerability_id]

    def list_vulnerabilities(self):
        return list(self.vulnerabilities.values())

    # Links between Equipments and Vulnerabilities
    def link(self, equipment_id, vulnerability_id):
        """Mark that a vulnerability affects an equipment."""
        equipment = self.get_equipment(equipment_id)
        vulnerability = self.get_vulnerability(vulnerability_id)
        if equipment is None:
            raise ValueError(f"Equipment ID {equipment_id} not found.")
        if vulnerability is None:
            raise ValueError(f"Vulnerability ID {vulnerability_id} not found.")
        if vulnerability_id in equipment.vulnerability_ids:
            raise ValueError(f"Vulnerability {vulnerability_id} is already linked to this equipment.")
        equipment.add_vulnerability(vulnerability_id)

    def unlink(self, equipment_id, vulnerability_id):
        """Mark that a vulnerability no longer affects an equipment."""
        equipment = self.get_equipment(equipment_id)
        if equipment is None:
            raise ValueError(f"Equipment ID {equipment_id} not found.")
        if vulnerability_id not in equipment.vulnerability_ids:
            raise ValueError(f"Vulnerability {vulnerability_id} is not linked to this equipment.")
        equipment.remove_vulnerability(vulnerability_id)

    def vulnerabilities_of(self, equipment_id):
        """Return the Vulnerability objects that affect an equipment."""
        equipment = self.get_equipment(equipment_id)
        if equipment is None:
            raise ValueError(f"Equipment ID {equipment_id} not found.")
        return [self.get_vulnerability(v_id) for v_id in equipment.vulnerability_ids]    