# APIGuard Architecture Overview

## Core Classes

### OpenAPIParser

- `parse() -> APISpec`
- `_load_spec()`
- `-_parse_endpoints() -> List[APIEndpoint]`
- `-_parse_single_endpoint() -> APIEndpoint`
- `_resolve_parameters() -> List[Dict]`
- `_resolve_reference() -> Dict`
- `_parse_request_body() -> Dict`
- `_parse_security() -> List[Dict]`
- `_parse_responses() -> Dict[str, Dict]`

### SecurityScanner

- `scan(self, api_spec: APISpec) -> List[Vulnerability]`


### TestSelector

- `select_tests_for_endpoint(endpoint) -> List[type[BaseSecuritytest]]`


### BaseSecuritytest(ABC)

- `execute() -> List[Vulnerability] (abstract)`
- `is_applicable(endpoint) -> bool`
- `make_request(method, path: str, **kwargs) -> aiohttp.ClientResponse:`
- `create_vulnerability() -> Vulnerability`
- `_get_references() -> List[str]`