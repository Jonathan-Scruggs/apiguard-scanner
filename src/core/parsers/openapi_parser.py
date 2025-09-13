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
        self.components: Dict[str,Dict] = {} # Spec Resuable parts like security schemas and object schemas
        self.base_url = base_url
    def parse(self) -> APISpec:
        '''
        Public High Level Primary Method to Parse the APISpec 
        '''
        self._load_spec()

        self._extract_components()

        endpoints = self._parse_endpoints()
        info = self.spec_data.get('info', {})

        title = info.get('title',{})
        version = info.get('version', {})
        print("Components", self.components)
        return APISpec(
            endpoints=endpoints,
            base_url=self.base_url,
            title=title,
            version=version
        )

    def _load_spec(self):
        '''
        Internal class method used to load(open) the spec and perform basic validation on it.
        '''
        try:
            with open(self.spec_path,'r') as file: 
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
        endpoints = []
        paths: Dict[str,Dict[str,Any]] = self.spec_data.get('paths', {})
        for path, methods in paths.items():
            for method, details in methods.items():
                if method.lower() in ['post','get','put','patch', 'delete', 'head', 'options']:
                    endpoint = self._parse_single_endpoint(path=path,method=method, details=details)
                    endpoints.append(endpoint)

        return endpoints
    


    def _parse_single_endpoint(self, path: str, method: str, details: Dict) -> APIEndpoint:
        '''
        Parses a Single Endpoint
        '''
        pass

        # 1.) Resolve parameters for that combination of path + method
        parameters = self._resolve_parameters(details.get('parameters', []))

        # 2.) Resolve request body
        request_body = self._parse_request_body(details.get('requestBody',{}))

        # 3.) Parse Security Information about this combination of path + method
        security_info = self._parse_security(details.get('security', []))

        responses = self._parse_responses(details.get('responses', {}))
        return APIEndpoint(
                            path=path,
                            method=method.upper(),
                            parameters=parameters,
                            security=security_info,
                            request_body=request_body,
                            summary=details.get('summary',''),
                            responses=responses
                            )
    def _resolve_parameters(self, parameters: List) -> List[Dict]:
        '''
        Resolves Paramter references and extracts full schemas for those parameters.
        '''
        resolved_parameters = [] 
        for param in parameters:
            if '$ref' in param:
                ref_path = param['$ref']
                resolved_param = self._resolve_reference(ref_path=ref_path)
                resolved_parameters.append(resolved_param)
            else:
                # Extracting Parameter Details
                param_info = {
                    'name': param.get('name'),
                    'in': param.get('in'),
                    'required': param.get('required', False),
                    'schema': param.get('schema', {}),
                    'style': param.get('style'),
                    'explode': param.get('explode'),
                    'description': param.get('description')
                }
                resolved_parameters.append(param_info)

        return resolved_parameters
    def _resolve_reference(self, ref_path: str) -> Dict:
        '''Resolves $ref to actual content.'''
        if ref_path.startswith("#/"):
            # parts of path to reference
            path_parts = ref_path[2:].split('/')
            current = self.spec_data

            for path in path_parts:
                current = current.get(path,{})
            
            return current
        else:
            raise ValueError(f"References to External Parameters is not supported: {ref_path}")

    def _parse_request_body(self, request_body: Dict) -> Dict:
        '''Parses the request body for endpoints that accept multiple content types'''
        if not request_body: # Request body has a falsy value
            return {}
        
        parsed_body =  {
            'required': request_body.get('required', False),
            'content_types': {}
        }

        content = request_body.get('content',{})

        for content_type, details in content.items():
            parsed_body['content_types'][content_type] = {
                'schema': details.get('schema', {}),
                'examples': details.get('examples', {})
            }
        return parsed_body
    
    def _parse_security(self, security: List) -> List[Dict]:
        """Parse security requirements with scopes"""
        parsed_security = []

        for security_req in security:
            parsed_req = {}
            for scheme_name, scopes in security_req.items():
                parsed_req[scheme_name] = {
                    'scopes': scopes,
                    'scheme_details': self.components.get('securitySchemes', {}).get(scheme_name, {})
                }

            parsed_security.append(parsed_req)
        return parsed_security
    def _parse_responses(self, responses: Dict) -> Dict[str, Dict]:
        """Parse response definitions"""
        parsed_responses = {}
        
        for status_code, response_def in responses.items():
            parsed_response = {
                'description': response_def.get('description', ''),
                'content_types': {},
                'headers': response_def.get('headers', {})
            }
            content = response_def.get('content', {})
            for content_type, content_details in content.items():
                schema = content_details.get('schema', {})
                examples = content_details.get('examples', {})
                
                parsed_response['content_types'][content_type] = {
                    'schema': schema,
                    'examples': examples
                }
            
            parsed_responses[status_code] = parsed_response
        
        return parsed_responses