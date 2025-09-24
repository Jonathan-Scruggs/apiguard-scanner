import pytest
from pathlib import Path
from src.core.parsers.openapi_parser import OpenAPIParser

class TestOpenApiParser:
    """Class of Tests that Test the open api parser."""
    def test_parse_simple_spec(self):
        """Test that tests the parsing a basic OpenAPI spec."""
        parser = OpenAPIParser('tests/fixtures/simple-spec.yaml','https://api.example.com')
        api_spec = parser.parse()

        assert api_spec.title == "Test API"
        assert api_spec.version == "1.0.0"
        assert api_spec.base_url == "https://api.example.com"
        assert len(api_spec.endpoints) == 3

    def test_parse_complex_spec_with_parameters(self):
        """Test parsing complex spec with parameters and security schemes"""
        parser = OpenAPIParser('tests/fixtures/complex-spec.yaml','https://api.example.com')
        api_spec = parser.parse()
        # Checking the Title and Number Of Endpoints
        assert api_spec.title == "Complex Test API"
        assert len(api_spec.endpoints) == 6

        
