from typing import List, Type
from ...security_tests.base_test import BaseSecurityTest


# Temporarily going to import tests manually to simplify pipeline(MVP)

class TestSelector:

    def __init__(self, config):
        self.config = config
        self.available_tests: List[type[BaseSecurityTest]] = [

        ] # Temporary list that stores all the tests that we can run in future will be the actual Test Catalog

    def select_tests_for_endpoint(self, endpoint) -> List[type[BaseSecurityTest]]:
        '''
        Intelligently determines what tests from the test catalog are appropriate to run on the endpoint.
        All the tests are of type base class BaseSecuritytest
        '''
        # TODO
        applicable_tests:List[type[BaseSecurityTest]] = [] # Annotation
        for test_class in self.available_tests:
            # Temporary instance with temporary arguements so we can call is_applicable
            test_class_instance = test_class(endpoint=endpoint,target_url=" ",session=None,config=self.config) 

            if test_class_instance.is_applicable():
                applicable_tests.append(test_class)

        # Sorting Tests By Priority so higher priority tests are run first

        sorted(applicable_tests, key=lambda test: test.priority)

        return applicable_tests