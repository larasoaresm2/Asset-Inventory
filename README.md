# Asset Inventory

An IT asset inventory manager, written in Python, that tracks assets and their associated vulnerabilities through a terminal menu, with data persisted in text files.

First graded assignment (sprints 1 and 2) for the Cybersecurity course — School of Electrical Engineering, UFU, 2026/2.

## Features

- **Create** IT assets with a unique identifier, name/hostname, owner, department, type and description
- **Read** an asset by its identifier or by its name
- **Update** the data of a registered asset
- **Delete** an asset, removing its vulnerabilities as well
- **List** all registered assets
- **Register vulnerabilities** for an asset, with description, category, severity and remediation status
- **List** the vulnerabilities of an asset, or report that it has none
- **Update** the remediation status of a vulnerability
- Error handling on every input: empty fields, invalid types, out-of-range options and duplicate identifiers

## How to run

Requirement: Python 3.

```bash
git clone https://github.com/larasoaresm2/Asset-Inventory.git
cd Asset-Inventory
python3 main.py
```

Run it from the project root, since the data files are read from and written to the `db/` folder.

## Data structures

| Structure | Where it is used | Why |
| --- | --- | --- |
| `Enum` (`AssetType`) | Asset types: NOTEBOOK, SERVER, ROUTER, WEB_APPLICATION, DATABASE | A fixed catalog in which each type carries an integer code used as its reference in the system |
| `Enum` (`Severity`, `Status`) | Severity levels (LOW, MEDIUM, HIGH, CRITICAL) and remediation statuses (OPEN, IN_PROGRESS, FIXED, RISK_ACCEPTED) | Fixed options that the user only picks from; each one is saved to the file by its integer code |
| Dictionary (`assets`) | Registered assets, indexed by identifier | Direct lookup by ID, with no need to traverse a list |
| List (`vulnerabilities`) | Vulnerabilities inside each asset | Grows as new vulnerabilities are registered |

## Persistence

Data lives in two text files in the `db/` folder, one record per line, with fields separated by `;`.

`db/assets.txt` — `id;name;owner;department;type code;description`

```
10;srv-01;Ana;IT;2;Main server
```

`db/vulnerabilities.txt` — `asset id;description;category;severity code;status code`

```
10;No updates;Outdated software;3;1
```

The first field of `vulnerabilities.txt` is the identifier of the asset that owns the vulnerability, and it is what links the two files. Severity and status are stored as the integer codes of the `Severity` and `Status` enums (in the example, `3` = HIGH and `1` = OPEN).

`load_data()` reads both files when the program starts; `save_data()` rewrites both after every change. This is why user input cannot contain `;`, the field separator.

## Code organization

The program is split into modules:

| Module | Content |
| --- | --- |
| `enums.py` | Fixed catalogs: `AssetType`, `Severity`, `Status` |
| `constants.py` | File paths (`ASSETS_FILE`, `VULNS_FILE`) and the field `SEPARATOR` |
| `helpers.py` | Input handling: `read_text()`, `read_int()`, `choose_from_list()`, `choose_asset_type()`, `ask_yes_no()` |
| `database.py` | The `assets` dictionary, `load_data()` and `save_data()` |
| `assets.py` | Asset CRUD: `find_asset()`, `show_asset()`, `list_assets()`, `create_asset()`, `read_asset()`, `update_asset()`, `delete_asset()` |
| `vulnerabilities.py` | `create_vulnerability()`, `add_vulnerability()`, `list_vulnerabilities()`, `update_vulnerability_status()` |
| `main.py` | Entry point: `main()`, with the menu |
| `db/` | Data files `assets.txt` and `vulnerabilities.txt` |

## Development

The assignment was developed in branches, each merged into `main` at the end of its stage:

| Branch | Content |
| --- | --- |
| `feature/base` | Enum, tuples, dictionary, input functions with error handling, and the menu |
| `feature/assets` | File reading and writing, asset CRUD and vulnerabilities |
| `docs/readme` | Project documentation |
| `refactor/clean-comments` | Split the single `asset_manager.py` file into modules |
| `docs/update-after-refactor` | Removed the old `asset_manager.py` and updated the documentation for the module layout |

## Author

Lara Soares — Federal University of Uberlândia