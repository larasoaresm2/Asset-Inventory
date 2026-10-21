"""Tests for the rules enforced by Inventory."""

import pytest

from asset_inventory.dependency import Dependency
from asset_inventory.equipment import Notebook, Server
from asset_inventory.inventory import Inventory
from asset_inventory.vulnerability import Vulnerability


@pytest.fixture
def inventory():
    """An inventory with two equipments and one vulnerability, new for each test."""
    inventory = Inventory()
    inventory.add_equipment(Server(1, "Web01", "Lara", "Lab", "web server"))
    inventory.add_equipment(Notebook(2, "Laptop", "Lara", "Home", "notebook"))
    inventory.add_vulnerability(Vulnerability(10, "SQL injection", "Web", 9.8))
    return inventory


@pytest.mark.parametrize("equipment_id", [1, 0, -5])
def test_equipment_id_must_be_new_and_positive(inventory, equipment_id):
    with pytest.raises(ValueError):
        inventory.add_equipment(Server(equipment_id, "Other", "Lara", "Lab", "test"))


@pytest.mark.parametrize("name", ["WEB01", "web01", "123"])
def test_name_must_be_unique_and_not_only_digits(inventory, name):
    with pytest.raises(ValueError):
        inventory.add_equipment(Server(3, name, "Lara", "Lab", "test"))


def test_get_equipment_by_id_or_by_name(inventory):
    assert inventory.get_equipment(1).name == "Web01"
    assert inventory.get_equipment("laptop").id == 2
    assert inventory.get_equipment(99) is None


def test_link_and_unlink(inventory):
    inventory.link(1, 10)
    assert inventory.vulnerabilities_of(1)[0].id == 10
    with pytest.raises(ValueError):
        inventory.link(1, 10)
    inventory.unlink(1, 10)
    assert inventory.vulnerabilities_of(1) == []
    with pytest.raises(ValueError):
        inventory.unlink(1, 10)


def test_removing_a_vulnerability_unlinks_it(inventory):
    inventory.link(1, 10)
    inventory.remove_vulnerability(10)
    assert inventory.get_equipment(1).vulnerability_ids == []


def test_removing_an_equipment_removes_its_dependencies(inventory):
    inventory.add_dependency(Dependency(2, 1, 0.5))
    inventory.remove_equipment(1)
    assert inventory.list_dependencies() == []


def test_dependency_needs_existing_equipments(inventory):
    with pytest.raises(ValueError):
        inventory.add_dependency(Dependency(2, 99, 0.5))


def test_row_sum_of_a_must_stay_below_1(inventory):
    inventory.add_equipment(Server(3, "Db01", "Lara", "Lab", "test"))
    inventory.add_dependency(Dependency(3, 1, 0.6))
    with pytest.raises(ValueError):
        inventory.add_dependency(Dependency(3, 2, 0.4))
    assert inventory.inherited_fraction(3) == pytest.approx(0.6)
