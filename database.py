from constants import ASSETS_FILE, SEPARATOR, VULNS_FILE
from enums import AssetType, Severity, Status

assets = {}

def load_data():
    """Read the text file and fills the assets dictionary"""
    try: 
        with open(ASSETS_FILE, "r", encoding="utf-8") as file:  
            for line in file:  
                line = line.strip() 
                if line == "":  
                    continue
                asset_id, name, owner, location, type_code, description = line.split(SEPARATOR)  
                assets[int(asset_id)] = {  
                    "id": int(asset_id),
                    "name": name,
                    "owner": owner,
                    "location": location,
                    "type": AssetType(int(type_code)),  
                    "description": description,
                    "vulnerabilities": []  
                }
    except FileNotFoundError:
        pass  

    try:
        with open(VULNS_FILE, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                asset_id, description, category, severity, status = line.split(SEPARATOR)
                asset_id = int(asset_id)
                if asset_id in assets:                 
                    assets[asset_id]["vulnerabilities"].append({
                        "description": description,
                        "category": category,
                        "severity": Severity(int(severity)),
                        "status": Status(int(status)),
                    })
    except FileNotFoundError:
        pass


def save_data():
    """Rewrites the text file with the current content of the dictionary"""
    with open(ASSETS_FILE, "w", encoding="utf-8") as file:  
        for asset in assets.values(): 
            fields = [str(asset["id"]), asset["name"], asset["owner"], asset["location"], str(asset["type"].value), asset["description"]]  
            file.write(SEPARATOR.join(fields) + "\n")  

    with open(VULNS_FILE, "w", encoding="utf-8") as file:
        for asset in assets.values():
            for vuln in asset["vulnerabilities"]:
                fields = [str(asset["id"]), vuln["description"], vuln["category"],
                          str(vuln["severity"].value), str(vuln["status"].value)]
                file.write(SEPARATOR.join(fields) + "\n")