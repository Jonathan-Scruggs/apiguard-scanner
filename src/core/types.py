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
    responses: Dict[str, Dict] = {}
    request_body: Optional[Dict] = {}
    summary: Optional[str] = ""
    
    

'''
Represents the Parsed API Spec
'''
@dataclass 
class APISpec:
    endpoints: List[APIEndpoint]
    base_url: str
    title: str
    version: str