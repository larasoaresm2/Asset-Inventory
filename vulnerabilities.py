#Step6: Vulnerabilidades

from assets import find_asset
from database import assets, save_data
from enums import Severity, Status
from helpers import choose_from_list, read_int, read_text


def create_vulnerability(asset):
    """Registers one vulnerability for an asset already found."""
    vuln = {
        "description": read_text("Vulnerability description: "),
        "category": read_text("Category (e.g. weak password, outdated software): "),
        "severity": choose_from_list("Severity:", Severity),
        "status": choose_from_list("Status:", Status),
    }
    asset["vulnerabilities"].append(vuln)
    print("Vulnerability added.")


def add_vulnerability():
    """Menu option: finds the asset and adds a vulnerability to it."""
    if not assets:
        print("No assets registered.")
        return
    asset = find_asset()
    if asset is None:
        print("Asset not found.")
        return
    create_vulnerability(asset)
    save_data()


def print_vulnerabilities(asset):
    for number, vuln in enumerate(asset["vulnerabilities"], start=1):
        print(f"  {number}. {vuln['description']} | category: {vuln['category']} "
              f"| severity: {vuln['severity'].name} | status: {vuln['status'].name}")


def list_vulnerabilities():
    if not assets:
        print("No assets registered.")
        return
    asset = find_asset()
    if asset is None:
        print("Asset not found.")
        return

    if len(asset["vulnerabilities"]) == 0:
        print(f"The asset '{asset['name']}' has no registered vulnerabilities.")
        return

    print(f"Vulnerabilities of '{asset['name']}':")
    print_vulnerabilities(asset)


def update_vulnerability_status():
    if not assets:
        print("No assets registered.")
        return
    asset = find_asset()
    if asset is None:
        print("Asset not found.")
        return

    if len(asset["vulnerabilities"]) == 0:
        print(f"The asset '{asset['name']}' has no registered vulnerabilities.")
        return

    print(f"Vulnerabilities of '{asset['name']}':")
    print_vulnerabilities(asset)

    while True:
        choice = read_int("Choose the vulnerability number to update: ")
        if 1 <= choice <= len(asset["vulnerabilities"]):
            break
        print("  Error: option out of range.")

    vuln = asset["vulnerabilities"][choice - 1]
    vuln["status"] = choose_from_list("New status:", Status)
    save_data()
    print("Vulnerability status updated.")