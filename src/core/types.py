from typing import Dict, List
from typing import Optional
from attr import dataclass

'''
Represents a Parsed API Endpoint
'''
@dataclass
class APIEndpoint:
    path: str
    method: str
    parameters: List[Dict] = []
    security: List[Dict] = []
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