"""Tests for the domain classes: Equipment and subclasses, Vulnerability and Dependency."""

import pytest

from asset_inventory.dependency import Dependency
from asset_inventory.enums import Status
from asset_inventory.equipment import Database, Equipment, Notebook, Router, Server, WebApplication
from asset_inventory.vulnerability import Vulnerability


@pytest.mark.parametrize(
    "equipment_class, expected_factor",
    [
        (Equipment, 1.0),
        (Server, 1.2),
        (Notebook, 1.0),
        (Router, 1.3),
        (WebApplication, 1.5),
        (Database, 0.8),
    ],
)
def test_each_type_has_its_exposure_factor(equipment_class, expected_factor):
    equipment = equipment_class(1, "Asset", "Lara", "Lab", "test")
    assert equipment.exposure_factor() == expected_factor


def test_add_vulnerability_ignores_duplicates():
    server = Server(1, "Web01", "Lara", "Lab", "test")
    server.add_vulnerability(10)
    server.add_vulnerability(10)
    assert server.vulnerability_ids == [10]


def test_equipments_do_not_share_the_vulnerability_list():
    first = Server(1, "Web01", "Lara", "Lab", "test")
    second = Server(2, "Web02", "Lara", "Lab", "test")
    first.add_vulnerability(10)
    assert second.vulnerability_ids == []


@pytest.mark.parametrize("cvss", [-0.1, 10.1, 12])
def test_cvss_out_of_range_is_rejected(cvss):
    with pytest.raises(ValueError):
        Vulnerability(1, "SQL injection", "Web", cvss)


@pytest.mark.parametrize(
    "status, active",
    [
        (Status.OPEN, True),
        (Status.IN_PROGRESS, True),
        (Status.FIXED, False),
        (Status.RISK_ACCEPTED, False),
    ],
)
def test_only_open_and_in_progress_count_for_risk(status, active):
    vulnerability = Vulnerability(1, "SQL injection", "Web", 9.8, status)
    assert vulnerability.is_active() == active


def test_equipment_cannot_depend_on_itself():
    with pytest.raises(ValueError):
        Dependency(1, 1, 0.5)


@pytest.mark.parametrize("fraction", [0.0, 1.0, -0.2, 1.5])
def test_fraction_must_be_between_0_and_1(fraction):
    with pytest.raises(ValueError):
        Dependency(1, 2, fraction)
