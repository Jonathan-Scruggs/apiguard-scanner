from ast import Dict, List
from typing import Optional
from attr import dataclass

'''
Represents a Parsed API Endpoint
'''
@dataclass
class APIEndpoint:
    path: str
    method: str
    parameters: List[Dict] = None
    security: List[Dict] = None
    operation_id: Optional[str] = None


'''
Represents the Parsed API Spec
'''
@dataclass 
class APISpec:
    endpoints: List[APIEndpoint]
    base_url: str
    title: str
    version: str