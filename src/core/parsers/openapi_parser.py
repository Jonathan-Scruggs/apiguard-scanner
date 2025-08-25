"""
Parser Is A Class That can Be Instantiated. Contains methods for parsing the OPENAPI spec.
"""
from typing import Any, List
from typing import Dict
from core.types import APIEndpoint, APISpec
import yaml

class OpenAPIParser:
    def __init__(self, file_path: str, base_url: str):
        self.spec_path = file_path
        self.spec_data: Dict[str, Any] = {} # Raw Spec Data
        self.components = {} # Spec Resuable parts like security schemas and object schemas
        self.base_url = base_url
    def parse(self) -> APISpec:
        '''
        Public High Level Primary Method to Parse the APISpec 
        '''
        self._load_spec()

        self._extract_components()

        self._parse_endpoints()

    def _load_spec(self):
        '''
        Internal class method used to load(open) the spec and perform basic validation on it.
        '''
        try:
            with open('example-spec.yaml','r') as file: 
                if self.spec_path.endswith("yaml") or self.spec_path.endswith("yml"):
                    data = yaml.load(file, Loader=yaml.SafeLoader)
                    self.spec_data = data
                else:
                    raise ValueError("Invalid file format, please provide a  yml or yaml file.")

        except FileNotFoundError:
            print(f"Error: the file at path:{self.spec_path} wasn't found")
        
        except yaml.YAMLError as exc:
            print(f"Something went wrong parsing the YAML file: {exc}")

        # Checking to verify the the data is now in a dictionary format
        if not isinstance(data,dict):
            raise ValueError(f"The specified file {self.spec_path} wasn't successfully parsed into a dict")
        
        # TODO Checking to Verify the data parsed is a OPEN API API Spec and is Version 3.0+ 
        if 'openapi' not in self.spec_data:
            raise ValueError("Invalid OPENAPI spec: missing the 'openapi' field")
        
        version = self.spec_data['openapi']
        version_num = int(version.split(".")[0])
        if version_num < 3:
            # openapi spec version is not greater than 3 so our parser will not work
            raise ValueError(f"Unsupported OpenAPI version: {version}. Version 3+ required")
        
    def _extract_components(self):
        '''
        Extracts reuseable components
        '''
        self.components = self.spec_data.get('components', {}) # Default is empty dictionary since spec may not have components

    
    def _parse_endpoints(self) -> List[APIEndpoint]:
        '''
        Extracts all endpoints in the spec
        '''
        # TODO FINISH THIS METHOD

        endpoints = []
        paths: Dict[str,Dict[str,Any]] = self.spec_data.get('paths', {})
        for endpoint, methods in paths.items():
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
    