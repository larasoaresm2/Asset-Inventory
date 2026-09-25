from enum import Enum 

class AssetType(Enum):  
    NOTEBOOK = 1  
    SERVER = 2  
    ROUTER = 3  
    WEB_APPLICATION = 4  
    DATABASE = 5

class Severity(Enum):  
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class Status(Enum):
    OPEN = 1
    IN_PROGRESS = 2
    FIXED = 3
    RISK_ACCEPTED = 4  