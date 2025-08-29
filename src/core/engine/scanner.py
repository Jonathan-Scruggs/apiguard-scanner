from typing import List
from core.types import APISpec
from ..engine.test_selector import TestSelector
from ....src.security_tests.base_test import Vulnerability

class SecurityScanner:
    def __init__(self, config):
        self.config = config
        self.test_selector = TestSelector(config=config)
    

    async def scan(self, api_spec: APISpec) -> List[Vulnerability]:
        for endpoint in api_spec.endpoints:
            pass