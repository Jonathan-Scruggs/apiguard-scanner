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
    request_body: Optional[Dict] = None
    summary: Optional[str] = None
    responses: Dict[str, Dict] = None
    

'''
Represents the Parsed API Spec
'''
@dataclass 
class APISpec:
    endpoints: List[APIEndpoint]
    base_url: str
    title: str
    version: str