import asyncio
from typing import List
import aiohttp
from core.types import APIEndpoint, APISpec
from .test_selector import TestSelector
from ...security_tests.base_test import BaseSecurityTest, Vulnerability

class SecurityScanner:
    """
    Main scanning engine that runs all the security testing.
    Workflow Is As Follows:
    1.) Takes the Parsed API Sepc
    2.) Call Test Selector on each Endpoint 
    3.) Execute selected tests on all endpoints 
    4.) Returns vulnerability report
    """
    def __init__(self, target, config):
        self.target = target
        self.config = config
        self.test_selector = TestSelector(config=config)
        self.session = None # Will create the session in the __aenter__

    # Relevant Guide For https://www.geeksforgeeks.org/python/aenter-in-python/ and 
    async def __aenter__(self):
        '''Async context manager entry point'''
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.config.get('timeout', 30)) 
        )
        return self # Returning object we want to use inside block.
    
    async def __aexit__(self, exc_type, exc, tb):
        '''Async context manager exit'''
        if self.session:
            await self.session.close() # Closing the HTTP Client Session



    async def scan(self, api_spec: APISpec) -> List[Vulnerability]:
        '''
        Scans APISpec
        Relevant Documentation: https://docs.python.org/3/library/threading.html#semaphore-example
        '''    
        total_tests = 0
        for endpoint in api_spec.endpoints:
            applicable_tests = self.test_selector.select_tests_for_endpoint(endpoint)
            total_tests += len(applicable_tests)

        # User can later on set in the config the max number of concurrent tests they want to run
        semaphore = asyncio.Semaphore(self.config.get('max_concurrent'),40) 
        # Progress Tracking
        completed_tests = 0
        all_vulnerabilities = []
        failed_tests = []


        async def run_single_test(test_class: type[BaseSecurityTest], endpoint: APIEndpoint):
            
            nonlocal completed_tests # To declare that this variable is the completed tests in the scan(nearest enclosing scope)

            async with semaphore:
                
                test_name = test_class.name
                endpoint_str = f"{endpoint.method} {endpoint.path}"
                try: 
                    
                    test_instance = test_class(endpoint=endpoint, target_url=self.target,session=self.session)
                    vulnerabilites = await test_instance.execute()

                    completed_tests += 1
                    if completed_tests % 10 == 0 or completed_tests == total_tests:
                        progress = (completed_tests / total_tests) * 100
                    return vulnerabilites

                except asyncio.TimeoutError:
                    error = f"Test '{test_name}' timed out on {endpoint_str}"
                    failed_tests.append(error)
                    completed_tests += 1
                    return [] 

                except aiohttp.ClientError as e:
                    error = f"Network error in '{test_name}' on {endpoint_str}: {e}"
                    failed_tests.append(error)
                    completed_tests += 1
                    return []
                
                except Exception as e:
                    error = f"Test '{test_name}' failed on {endpoint_str}: {e}"
                    failed_tests.append(error)
                    completed_tests += 1
                    return []

        # Creating all the test tasks    
        all_tasks = []

        for endpoint in api_spec.endpoints:
            applicable_tests: List[type[BaseSecurityTest]] = self.test_selector.select_tests_for_endpoint(endpoint=endpoint)
            for test_class in applicable_tests:
                test_task = asyncio.create_task(run_single_test(test_class,endpoint))
                all_tasks.append(test_task)

        results = await asyncio.gather(*all_tasks, return_exceptions=True) # Waiting for all tasks to finish
        # TODO Hand off results to eventual report generator.
        