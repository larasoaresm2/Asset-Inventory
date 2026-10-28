"""Tests for the menu navigation, typing the answers with monkeypatch."""

from asset_inventory.equipment import Server
from asset_inventory.inventory import Inventory
from asset_inventory.menu import Menu
from asset_inventory.storage import JsonStorage


def type_answers(monkeypatch, answers):
    """Replace input() so that each call returns the next answer of the list."""
    answers = iter(answers)
    monkeypatch.setattr("builtins.input", lambda message="": next(answers))


def test_create_equipment_through_the_submenu_and_save(monkeypatch, tmp_path):
    inventory = Inventory()
    storage = JsonStorage(tmp_path / "data")
    type_answers(
        monkeypatch,
        [
            "1",  # main menu: Equipments
            "1",  # submenu: Create equipment
            "1",  # type: Server
            "7",  # ID
            "Web01",  # name
            "Lara",  # owner
            "Lab",  # location
            "web server",  # description
            "0",  # back
            "0",  # exit
        ],
    )
    Menu(inventory, storage).run()

    assert isinstance(inventory.get_equipment(7), Server)
    reloaded = Inventory()
    storage.load(reloaded)
    assert reloaded.get_equipment("web01").id == 7


def test_invalid_option_and_back(monkeypatch, capsys):
    type_answers(monkeypatch, ["9", "4", "0", "0"])  # invalid, Dependencies, back, exit
    Menu(Inventory()).run()
    output = capsys.readouterr().out
    assert "Invalid option" in output
    assert "==== DEPENDENCIES ====" in output
    assert "Goodbye!" in output


def test_failed_action_is_not_saved(monkeypatch, tmp_path):
    storage = JsonStorage(tmp_path / "data")
    type_answers(monkeypatch, ["1", "3", "99", "0", "0"])  # show equipment 99, which does not exist
    Menu(Inventory(), storage).run()
    assert not (tmp_path / "data").exists()
