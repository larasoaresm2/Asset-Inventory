class Equipment:
    """Base class: any IT asset in the inventory."""

    def __init__(self, equipment_id, name, owner, location, description, vulnerability_ids=None):
        self.id = equipment_id
        self.name = name
        self.owner = owner
        self.location = location
        self.description = description

        if vulnerability_ids is None:
            vulnerability_ids = []
        self.vulnerability_ids = vulnerability_ids

    def exposure_factor(self):
       """How much this type of equipment amplifies its own risk."""
       return 1.0

    def add_vulnerability(self, vulnerability_id):
        if vulnerability_id not in self.vulnerability_ids:
            self.vulnerability_ids.append(vulnerability_id)

    def remove_vulnerability(self, vulnerability_id):
        if vulnerability_id in self.vulnerability_ids:
            self.vulnerability_ids.remove(vulnerability_id)

    def __str__(self):
        return (f"[{self.id}] {self.name} ({type(self).__name__}) | "f"owner: {self.owner} | location: {self.location}")


class Server(Equipment):
    def exposure_factor(self):
        return 1.2


class Notebook(Equipment):
    def exposure_factor(self):
        return 1.0


class Router(Equipment):
    def exposure_factor(self):
        return 1.3


class WebApplication(Equipment):
    def exposure_factor(self):
        return 1.5


class Database(Equipment):
    def exposure_factor(self):
        return 0.8