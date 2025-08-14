"""
Parser Is A Class That can Be Instantiated. Contains methods for parsing the OPENAPI spec.

"""


from ast import List
from typing import Dict
from core.types import APIEndpoint, APISpec


class OpenAPIParser:
    def __init__(self, file_path: str):
        pass

    def parse(self) -> APISpec:
        '''
        High Level Primary Method to Parse the APISpec 
        '''
        pass

    def _load_spec(self):
        '''
        Internal class method used to load(open) the spec and perform basic validation on it.
        '''
        pass

    def _extract_components(self):
        '''
        Extracts reuseable components
        '''
        pass

    def _extract_base_url(self) -> str:
        '''
        Extracts the base/server url for the API
        '''
        pass
    def _parse_endpoints(self) -> List[APIEndpoint]:
        '''
        Extracts all endpoints in the spec
        '''
        pass

    def _parse_single_endpoint(self, path: str, method: str, details: Dict) -> APIEndpoint:
        '''
        Parses a Single Endpoint
        '''
        pass

    def _resolve_paramters(self, parameters: List) -> List[Dict]:
        '''
        Resolves Paramter references and extracts full schemas for those parameters.
        '''
        pass

    def _resolve_references(self, ref_path: str) -> Dict:
        '''Resolves $ref to actual content.'''
        pass 

    def _resolve_request_body(self, request_body: Dict) -> Dict:
        '''Parses the request body for endpoints that accept multiple content types'''
    pass
    
    def _parse_security(self, security: List) -> List[Dict]:
        """Parse security requirements with scopes"""
        pass
    