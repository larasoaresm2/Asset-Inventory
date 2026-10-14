import numpy as np

# Above this condition number, I - A is treated as numerically singular
MAX_CONDITION_NUMBER = 1e12


class RiskAnalysis:
    """Linear risk model.

    Own risk:        b = F M v
    Effective risk:  x = b + A x   <=>   (I - A) x = b
    """

    def __init__(self, inventory):
        self.inventory = inventory
        self.condition_number = None
        self.determinant = None

    def build_matrices(self):
        """Build M, v, F and A from the inventory, in a fixed order."""
        equipments = self.inventory.list_equipments()
        vulnerabilities = [v for v in self.inventory.list_vulnerabilities() if v.is_active()]

        equipment_index = {e.id: i for i, e in enumerate(equipments)}
        vulnerability_index = {v.id: j for j, v in enumerate(vulnerabilities)}
        n, m = len(equipments), len(vulnerabilities)
        M = np.zeros((n, m))
        for i, equipment in enumerate(equipments):
            for v_id in equipment.vulnerability_ids:
                if v_id in vulnerability_index:
                    M[i, vulnerability_index[v_id]] = 1.0
        v = np.array([vulnerability.cvss for vulnerability in vulnerabilities], dtype=float)
        F = np.diag([equipment.exposure_factor() for equipment in equipments])
        A = np.zeros((n, n))
        for dependency in self.inventory.list_dependencies():
            i = equipment_index[dependency.dependent_id]
            j = equipment_index[dependency.source_id]
            A[i, j] = dependency.fraction

        return equipments, M, v, F, A

    def compute(self):
        """Return [(equipment, own_risk, effective_risk), ...], highest risk first."""
        equipments, M, v, F, A = self.build_matrices()
        if not equipments:
            raise ValueError("No equipments registered.")

        b = F @ M @ v                     
        system = np.eye(len(equipments)) - A
        self.determinant = np.linalg.det(system)
        self.condition_number = np.linalg.cond(system)
        if not np.isfinite(self.condition_number) or self.condition_number > MAX_CONDITION_NUMBER:
            raise ValueError(
                f"I - A is singular or ill-conditioned (condition number "
                f"{self.condition_number:.2e}); the system was not solved.")

        x = np.linalg.solve(system, b)
        rows = list(zip(equipments, b, x))
        rows.sort(key=lambda row: row[2], reverse=True)
        return rows