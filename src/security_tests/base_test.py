"""
This the base test class and every other test inherits from this Base class.
"""
from abc import ABC, abstractmethod
from csv import Error
from enum import Enum
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from unicodedata import category
import asyncio 
import aiohttp

# Set of named values for the severity will be used like VulnerabilitySeverity.HIGH later on
class VulnerabilitySeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class TestPriority(Enum):
    CRITICAL = 1
    HIGH = 2 
    MEDIUM = 3
    LOW = 4


# Data Class That Will Store Data about A Vulnerability
@dataclass
class Vulnerability:
    id: str
    title: str
    description: str
    severity: VulnerabilitySeverity
    category: str
    cwe_id: Optional[str] = None # common weakness enumeration
    owasp_category: Optional[str] = None # OWASP mapping
    endpoint: Optional[str] = None
    method: Optional[str] = None# HTTP method
    evidence: Optional[Dict[str, Any]] | None = None
    remediation: Optional[str] = None
    references: List[str] = []
    confidence: float = 1.0 
    

class BaseSecurityTest(ABC):
    "Abstract Base Class for all Security Tests"

    # Test metadta that is overriden in subclass
    test_id: str = ""
    name: str = ""
    description: str = ""
    category: str = ""
    priority: TestPriority = TestPriority.MEDIUM # Setting a default test value of medium

    owasp_category: Optional[str] = None
    cwe_id: Optional[str] = None

    def __init__(self, endpoint, target_url, session, config):
        self.endpoint = endpoint
        self.target_url = target_url
        self.session = session
        self.config = config
        self.vulnerabilities = [] # Initially a endpoint can have 0 vulnerabilities

    @abstractmethod
    async def execute(self) -> List[Vulnerability]:
        """Executes the security test and returns a list of found vulnerabilities"""
        pass

    def is_applicable(self, endpoint) -> bool:
        """Simple method that checks if the current test is applicable to the provided endpoint."""
        return True
    
    async def make_request(self, method: str, path: str, **kwargs) -> aiohttp.ClientResponse:
        """Make HTTP request with proper error handling and logging"""
        url = f"{self.target_url}{path}"
        
        try:
            response = await self.session.request(method, url, **kwargs)
            return response
        except asyncio.TimeoutError:
            raise Error(f"Request timeout for {method} {url}")
        except Exception as e:
            raise Error(f"Request failed for {method} {url}: {e}")
        
    def create_vulnerability(
        self,
        title: str,
        description: str,
        severity: VulnerabilitySeverity,
        evidence: Dict[str, Any] = {},
        confidence: float = 1.0 # Default value of 1
    ) -> Vulnerability:
        """Helper function to create vulnerability objects"""

        return Vulnerability(
            id=f"{self.test_id}_{len(self.vulnerabilities)}",
            title=title,
            description=description,
            severity=severity,
            category=self.category,
            cwe_id=self.cwe_id,
            owasp_category=self.owasp_category,
            endpoint=f"{self.endpoint.method} {self.endpoint.path}",
            method=self.endpoint.method,
            evidence=evidence or {},
            confidence=confidence,
            references=self._get_references()
        )
    
    # Note: Internal Use method and not truly private.
    def _get_references(self) -> List[str]:
        """Gets the correct reference URLS for the vulnerability type"""
        # Example URL: https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/
        references = []
        if self.owasp_category:
            references.append(f"https://owasp.org/API-Security/editions/2023/en/{self.owasp_category.lower()}/")
        references.append("https://owasp.org/www-project-web-security-testing-guide/")

       
        return references