# Asset Inventory

An IT asset inventory manager written in Python, using object-oriented programming. It tracks equipments and vulnerabilities through a terminal menu, links each vulnerability to the equipments it affects, and will estimate the risk of each equipment with a linear-algebra model.

Second graded assignment (sprints 3, 4 and 5) for the Cybersecurity course — School of Electrical Engineering, UFU, 2026/2. The first assignment is preserved in the tag [`trabalho-1`](../../tree/trabalho-1).

## Assignment 2 requirements

| # | Requirement | Weight | Status |
| --- | --- | --- | --- |
| 1 | Each asset is an object of an equipment class hierarchy | 20% | Done |
| 2 | Data stored as a JSON array of objects | 20% | Planned |
| 3 | Application running in a Docker container for 24 hours | 45% | Planned |
| 4 | Effective risk of each equipment computed with a linear model | 15% | In progress |

## Features

- **Equipments:** create, list, show, update and delete. Search by ID or by name (case-insensitive)
- **Vulnerabilities:** create, list, update (description, category, CVSS and status) and delete
- **Links:** link and unlink a vulnerability to an equipment, and list the vulnerabilities of an equipment
- **Validation** while typing, asking again instead of losing what was already typed:
  - IDs must be positive integers and unique
  - Equipment names must be unique (ignoring case) and cannot contain only digits, so a search by name is never ambiguous or confused with an ID
  - CVSS must be a number between 0.0 and 10.0
  - Linking an already linked vulnerability, or unlinking one that is not linked, is rejected
- **Referential integrity:** deleting a vulnerability also unlinks it from every equipment; deleting an equipment keeps the vulnerabilities, since they may affect other equipments
- **Confirmation** before any deletion
- Clean exit with `Ctrl+C` or `Ctrl+D`

## How to run

Requirement: Python 3.10 or newer.

```bash
git clone https://github.com/larasoaresm2/Asset-Inventory.git
cd Asset-Inventory
python3 main.py
```

Data is kept in memory for now; JSON persistence is the next stage.

## Class design

```
Equipment (base class)
├── Server
├── Notebook
├── Router
├── WebApplication
└── Database

Vulnerability ── Status (Enum)

Inventory ── has many ──> Equipment, Vulnerability
Menu ── uses ──> Inventory
```

| Class | File | Responsibility |
| --- | --- | --- |
| `Equipment` and subclasses | `asset_inventory/equipment.py` | One IT asset: ID, name, owner, location, description and the IDs of the vulnerabilities that affect it |
| `Vulnerability` | `asset_inventory/vulnerability.py` | One security weakness: ID, description, category, CVSS score and status. Validates the CVSS score |
| `Status` | `asset_inventory/enums.py` | Remediation status: OPEN, IN_PROGRESS, FIXED, RISK_ACCEPTED |
| `Inventory` | `asset_inventory/inventory.py` | Stores all objects and enforces the business rules (unique IDs and names, links, integrity) |
| `Menu` | `asset_inventory/menu.py` | The only class that talks to the user (`print` and `input`) |
| — | `asset_inventory/helpers.py` | Input functions: `read_text()`, `read_int()`, `read_float()`, `choose_from_list()`, `ask_yes_no()` |
| — | `main.py` | Entry point: creates the `Inventory` and the `Menu` |

### Object-oriented concepts used

- **Inheritance:** each equipment type is a subclass of `Equipment` and reuses all its attributes and methods
- **Polymorphism:** every subclass overrides `exposure_factor()`, which will weight the equipment's own risk. The menu creates any type through the same call, `equipment_class(...)`
- **Composition:** `Inventory` *has* equipments and vulnerabilities; `Menu` *has* an `Inventory`
- **Encapsulation of rules:** validation lives in `Inventory` and `Vulnerability`, so it protects the data whatever the source (menu today, JSON file and web API later). The menu validates again while typing only to improve the user experience (defense in depth)

### Exposure factor by equipment type

| Type | Factor | Rationale |
| --- | --- | --- |
| `WebApplication` | 1.5 | Exposed to the internet by design |
| `Router` | 1.3 | Sits on the network perimeter, reachable from outside |
| `Server` | 1.2 | Exposes network services to many clients |
| `Notebook` | 1.0 | Reference value |
| `Database` | 0.8 | Should not be directly reachable; its risk arrives through the applications that depend on it |

The factor measures **exposure** only. How risk spreads from one equipment to another is modeled separately by the dependency matrix of the risk model, so it is not counted twice.

## Development

Each stage is developed in its own branch and merged into `main` through a pull request.

| Branch | Content |
| --- | --- |
| `feature/base`, `feature/assets`, `docs/readme`, `refactor/clean-comments`, `docs/update-after-refactor` | Assignment 1 (see tag `trabalho-1`) |
| `refactor/oop-models` | Rewrite in object-oriented programming: classes, inheritance, polymorphism and the new menu |
| `feat/risk-analysis` | Dependencies between equipments and the risk model with NumPy *(next)* |
| `feat/json-storage` | JSON persistence *(planned)* |
| `feat/docker` | Dockerfile and container execution *(planned)* |


## Author

Lara Soares — Federal University of Uberlândia