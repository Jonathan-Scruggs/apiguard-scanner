"""
Parser Is A Class That can Be Instantiated. Contains methods for parsing the OPENAPI spec.
"""
from ast import List
from typing import Dict
from core.types import APIEndpoint, APISpec
import yaml

class OpenAPIParser:
    def __init__(self, file_path: str):
        self.spec_path = file_path
        self.spec_data = None # Raw Spec Data
        self.components = {} # Spec Resuable parts like security schemas and object schemas

    def parse(self) -> APISpec:
        '''
        Public High Level Primary Method to Parse the APISpec 
        '''
        pass

    def _load_spec(self):
        '''
        Internal class method used to load(open) the spec and perform basic validation on it.
        '''
        try:
            with open('example-spec.yaml','r') as file: 
                if self.spec_path.endswith("yaml") or self.spec_path.endswith("yml"):
                    data = yaml.load(file, Loader=yaml.SafeLoader)
                else:
                    raise ValueError("Invalid file format, please provide a  yml or yaml file.")

        except FileNotFoundError:
            print(f"Error: the file at path:{self.spec_path} wasn't found")
        
        except yaml.YAMLError as exc:
            print(f"Something went wrong parsing the YAML file: {exc}")

        # Checking to verify the the data is now in a dictionary format
        if not isinstance(data,dict):
            raise ValueError(f"The specified file {self.spec_path} wasn't successfully parsed into a dict")
        
        # Checking to Verify the data parsed is a OPEN API API Spec and is Version 3.0+ 
        print(data)


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
    