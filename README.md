# Asset Inventory

An IT asset inventory manager, written in Python, that tracks assets and their associated vulnerabilities through a terminal menu, with data persisted in text files.

First graded assignment (sprints 1 and 2) for the Cybersecurity course — School of Electrical Engineering, UFU, 2026/2.

## Features

- **Create** IT assets with a unique identifier, name/hostname, owner, department, type and description
- **Read** an asset by its identifier or by its name
- **Update** the data of a registered asset
- **Delete** an asset, removing its vulnerabilities as well
- **Register vulnerabilities** for an asset, with description, category, severity and remediation status
- **List** the vulnerabilities of an asset, or report that it has none
- Error handling on every input: empty fields, invalid types, out-of-range options and duplicate identifiers

## How to run

Requirement: Python 3.

```bash
git clone https://github.com/larasoaresm2/Asset-Inventory.git
cd Asset-Inventory
python3 asset_manager.py
```

The data files are created automatically on the first save.

## Data structures

| Structure | Where it is used | Why |
| --- | --- | --- |
| `Enum` (`AssetType`) | Asset types: NOTEBOOK, SERVER, ROUTER, WEB_APPLICATION, DATABASE | A fixed catalog in which each type carries an integer code used as its reference in the system |
| Tuple (`SEVERITIES`, `STATUSES`) | Severity levels and remediation statuses | Fixed options that the user only picks from and the program never changes |
| Dictionary (`assets`) | Registered assets, indexed by identifier | Direct lookup by ID, with no need to traverse a list |
| List (`vulnerabilities`) | Vulnerabilities inside each asset | Grows as new vulnerabilities are registered |

## Persistence

Data lives in two text files, one record per line, with fields separated by `;`.

`assets.txt` — `id;name;owner;department;type code;description`

```
10;srv-01;Ana;IT;2;Main server
```

`vulnerabilities.txt` — `asset id;description;category;severity;status`

```
10;No updates;Outdated software;high;open
```

The first field of `vulnerabilities.txt` is the identifier of the asset that owns the vulnerability, and it is what links the two files.

`load_data()` reads both files when the program starts; `save_data()` rewrites both after every change. This is why user input cannot contain `;`, the field separator.

## Code organization

The program lives in a single file, `asset_manager.py`, split into blocks:

1. Fixed structures: `AssetType`, `SEVERITIES`, `STATUSES`, the file constants and the `assets` dictionary
2. Input handling: `read_text()`, `read_int()`, `choose_from_list()`, `choose_asset_type()`, `ask_yes_no()`
3. Files: `load_data()` and `save_data()`
4. Asset CRUD: `find_asset()`, `show_asset()`, `create_asset()`, `read_asset()`, `update_asset()`, `delete_asset()`
5. Vulnerabilities: `create_vulnerability()`, `add_vulnerability()`, `list_vulnerabilities()`
6. Interface: `main()`, with the menu

## Development

The assignment was developed in branches, each merged into `main` at the end of its stage:

| Branch | Content |
| --- | --- |
| `feature/base` | Enum, tuples, dictionary, input functions with error handling, and the menu |
| `feature/assets` | File reading and writing, asset CRUD and vulnerabilities |
| `docs/readme` | Project documentation |

## Author

Lara Soares — Federal University of Uberlândia