"""Tests for the risk model: b = F M v and (I - A) x = b."""

import numpy as np
import pytest

from asset_inventory.dependency import Dependency
from asset_inventory.enums import Status
from asset_inventory.equipment import Notebook, Server
from asset_inventory.inventory import Inventory
from asset_inventory.risk import RiskAnalysis
from asset_inventory.vulnerability import Vulnerability


@pytest.fixture
def scenario():
    """The scenario solved by hand in the README: x = [8.98, 14.8, 7.45]."""
    inventory = Inventory()
    for equipment_id, name in [(1, "E1"), (2, "E2"), (3, "E3")]:
        inventory.add_equipment(Notebook(equipment_id, name, "Lara", "Lab", "test"))
    inventory.add_vulnerability(Vulnerability(1, "V1", "Web", 7.5))
    inventory.add_vulnerability(Vulnerability(2, "V2", "Web", 5.0))
    inventory.add_vulnerability(Vulnerability(3, "V3", "Web", 9.8))
    inventory.link(1, 1)
    inventory.link(2, 2)
    inventory.link(2, 3)
    inventory.add_dependency(Dependency(1, 2, 0.1))
    inventory.add_dependency(Dependency(3, 1, 0.5))
    inventory.add_dependency(Dependency(3, 2, 0.2))
    return inventory


def risks_by_name(inventory):
    """Run the analysis and return {name: (own risk, effective risk)}."""
    rows = RiskAnalysis(inventory).compute()
    return {equipment.name: (own, effective) for equipment, own, effective in rows}


def test_scenario_solved_by_hand(scenario):
    risks = risks_by_name(scenario)
    assert risks["E1"] == pytest.approx((7.5, 8.98))
    assert risks["E2"] == pytest.approx((14.8, 14.8))
    assert risks["E3"] == pytest.approx((0.0, 7.45))


def test_report_is_sorted_by_effective_risk(scenario):
    rows = RiskAnalysis(scenario).compute()
    assert [equipment.name for equipment, _, _ in rows] == ["E2", "E1", "E3"]


def test_matrices_have_the_right_shape(scenario):
    equipments, M, v, F, A = RiskAnalysis(scenario).build_matrices()
    assert M.shape == (3, 3)
    assert A[0, 1] == pytest.approx(0.1)
    assert np.allclose(np.diag(F), [1.0, 1.0, 1.0])


def test_exposure_factor_multiplies_own_risk():
    inventory = Inventory()
    inventory.add_equipment(Server(1, "Web01", "Lara", "Lab", "test"))
    inventory.add_vulnerability(Vulnerability(1, "V1", "Web", 10.0))
    inventory.link(1, 1)
    assert risks_by_name(inventory)["Web01"] == pytest.approx((12.0, 12.0))


def test_fixed_vulnerability_does_not_count(scenario):
    scenario.get_vulnerability(1).status = Status.FIXED
    assert risks_by_name(scenario)["E1"][0] == pytest.approx(0.0)


def test_condition_number_is_stored(scenario):
    analysis = RiskAnalysis(scenario)
    analysis.compute()
    assert analysis.condition_number == pytest.approx(1.728, abs=1e-3)


def test_singular_system_is_refused(scenario):
    # Bypass the Inventory rule on purpose to force I - A to be singular
    scenario.dependencies[(1, 2)].fraction = 1.0
    reverse = Dependency(2, 1, 0.5)
    reverse.fraction = 1.0
    scenario.dependencies[(2, 1)] = reverse
    with pytest.raises(ValueError):
        RiskAnalysis(scenario).compute()


def test_empty_inventory_is_refused():
    with pytest.raises(ValueError):
        RiskAnalysis(Inventory()).compute()
