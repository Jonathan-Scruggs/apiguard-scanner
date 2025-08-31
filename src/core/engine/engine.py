import asyncio
from typing import List
import aiohttp
from core.types import APISpec
from .test_selector import TestSelector
from ...security_tests.base_test import Vulnerability

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
        test_tasks = []
        # Gathering all the test coroutines
        for endpoint in api_spec.endpoints:
            applicable_tests = self.test_selector.select_tests_for_endpoint(endpoint=endpoint)

            async with asyncio.TaskGroup() as tg:
                 for test_class in applicable_tests:
                    test_instance = test_class(endpoint=endpoint, target_url=self.target,session=self.session,config=self.config) 
                    test_task = tg.create_task(test_instance.execute())
                    test_tasks.append(test_task)

        # After this point all tasks are complete 