"""Tests for JsonStorage: save, reload and broken files."""

import json

import pytest

from asset_inventory.dependency import Dependency
from asset_inventory.enums import Status
from asset_inventory.equipment import Router, Server
from asset_inventory.inventory import Inventory
from asset_inventory.storage import JsonStorage
from asset_inventory.vulnerability import Vulnerability


@pytest.fixture
def storage(tmp_path):
    """A JsonStorage in a temporary folder that pytest deletes after the test."""
    return JsonStorage(tmp_path / "data")


@pytest.fixture
def inventory():
    inventory = Inventory()
    inventory.add_equipment(Server(1, "Servidor Ação", "Lara", "Lab", "web server"))
    inventory.add_equipment(Router(2, "Edge", "Lara", "Rack", "router"))
    inventory.add_vulnerability(Vulnerability(10, "Injeção SQL", "Web", 9.8))
    inventory.add_vulnerability(Vulnerability(11, "Old TLS", "Crypto", 5.3, Status.FIXED))
    inventory.link(1, 10)
    inventory.link(2, 11)
    inventory.add_dependency(Dependency(2, 1, 0.4))
    return inventory


def reload(storage):
    new_inventory = Inventory()
    storage.load(new_inventory)
    return new_inventory


def test_files_are_json_arrays(storage, inventory):
    storage.save(inventory)
    with open(storage.equipments_file, encoding="utf-8") as file:
        data = json.load(file)
    assert isinstance(data, list)
    assert data[0]["type"] == "Server"
    assert data[0]["name"] == "Servidor Ação"


def test_reload_keeps_types_ids_links_and_status(storage, inventory):
    storage.save(inventory)
    loaded = reload(storage)
    assert isinstance(loaded.get_equipment(1), Server)
    assert isinstance(loaded.get_equipment(2), Router)
    assert loaded.get_equipment(2).vulnerability_ids == [11]
    assert loaded.get_vulnerability(11).status == Status.FIXED
    assert loaded.inherited_fraction(2) == pytest.approx(0.4)


def test_missing_folder_starts_empty(storage):
    loaded = reload(storage)
    assert loaded.list_equipments() == []


def test_empty_file_counts_as_empty_list(storage):
    storage.save(Inventory())
    with open(storage.equipments_file, "w", encoding="utf-8") as file:
        file.write("")
    assert reload(storage).list_equipments() == []


@pytest.mark.parametrize(
    "content",
    [
        "[{broken",  # not valid JSON
        '{"id": 1}',  # valid JSON, but not an array
        '[{"type": "Server", "id": 1}]',  # missing fields
        '[{"type": "Laptop", "id": 1, "name": "x", "owner": "", "location": "", '
        '"description": "", "vulnerability_ids": []}]',  # unknown type
    ],
)
def test_broken_equipment_file_is_refused(storage, content):
    storage.save(Inventory())
    with open(storage.equipments_file, "w", encoding="utf-8") as file:
        file.write(content)
    with pytest.raises(ValueError):
        reload(storage)


def test_invalid_data_is_refused_by_the_rules(storage):
    storage.save(Inventory())
    with open(storage.vulnerabilities_file, "w", encoding="utf-8") as file:
        json.dump(
            [{"id": 1, "description": "x", "category": "y", "cvss": 12, "status": "OPEN"}], file
        )
    with pytest.raises(ValueError):
        reload(storage)


def test_write_leaves_no_temporary_file(storage, inventory):
    storage.save(inventory)
    leftovers = [path.name for path in (storage.folder).iterdir() if path.suffix == ".tmp"]
    assert leftovers == []
