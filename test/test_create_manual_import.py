# coding: utf-8

"""
    Deep Lynx

    The construction of megaprojects has consistently demonstrated challenges for project managers in regard to meeting cost, schedule, and performance requirements. Megaproject construction challenges are common place within megaprojects with many active projects in the United States failing to meet cost and schedule efforts by significant margins. Currently, engineering teams operate in siloed tools and disparate teams where connections across design, procurement, and construction systems are translated manually or over brittle point-to-point integrations. The manual nature of data exchange increases the risk of silent errors in the reactor design, with each silent error cascading across the design. These cascading errors lead to uncontrollable risk during construction, resulting in significant delays and cost overruns. Deep Lynx allows for an integrated platform during design and operations of mega projects.  The Deep Lynx Core API delivers a few main features.  1. Provides a set of methods and endpoints for manipulating data in an object oriented database. This allows us to store complex datatypes as records and then to compile them into actual, modifiable objects at run-time. Users can store taxonomies or ontologies in a readable format.  2. Provides methods for storing and retrieving data in a graph database. This data is structured and validated against the aformentioned object oriented database before storage.  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import
from os import getenv
from dotenv import load_dotenv

import unittest
from deep_lynx.configuration import Configuration
from deep_lynx.models.create_container_request import CreateContainerRequest
from deep_lynx.models.create_container_response import CreateContainerResponse
from deep_lynx.models.create_data_source_request import CreateDataSourceRequest
from deep_lynx.models.token_exchange_request import TokenExchangeRequest

import swagger_client
import deep_lynx
from swagger_client.models.create_manual_import import CreateManualImport  # noqa: E501
from swagger_client.rest import ApiException


class TestCreateManualImport(unittest.TestCase):
    """CreateManualImport unit test stubs"""

    # API Setup
    configuration = Configuration()
    configuration.host = 'http://localhost:8090'
    apiClient = deep_lynx.ApiClient(configuration)

    containerApi = deep_lynx.ContainersApi(apiClient)
    containerId = ''

    def setUp(self):
        load_dotenv()
        if getenv('API_KEY') is None or getenv('API_SECRET') is None:
            print("""Please supply API key and secret.
Have you copied the .env-sample and created .env?
Skipping all tests in test_create_manual_import.py""")
            raise unittest.SkipTest("""Please supply API key and secret.
                Have you copied the .env-sample and created .env?
                Skipping all tests in test_create_manual_import.py""")
                
        if getenv('API_KEY') == '' or getenv('API_SECRET') == '':
            print("""Please supply API key and secret.
Skipping all tests in test_create_manual_import.py""")
            raise unittest.SkipTest("""Please supply API key and secret.
                Skipping all tests in test_create_manual_import.py""")
        pass

    def tearDown(self):
        if self.containerId != '':
            self.containerApi.archive_container(self.containerId, permanent=True)
            print('Successfully removed test container')
        pass

    def testCreateManualImport(self):
        """Test CreateManualImport"""
        # Verify API keys have been provided
        apiKey = getenv('API_KEY')
        apiSecret = getenv('API_SECRET')

        # Authenticate
        authApi = deep_lynx.AuthenticationApi(self.apiClient)

        token = authApi.retrieve_o_auth_token(x_api_key=apiKey, x_api_secret=apiSecret, x_api_expiry='1h')
        self.assertIsNotNone(token)

        container = self.containerApi.create_container(CreateContainerRequest(
            'sdk_test', 'Test container description', False
        ))
        self.assertIsNotNone(container.value[0].id)
        self.containerId = container.value[0].id

        # Create Data Source
        datasourcesApi = deep_lynx.DataSourcesApi(self.apiClient)

        datasource = datasourcesApi.create_data_source(CreateDataSourceRequest(
            'sdk_test_source', 'standard', True
        ), self.containerId)
        self.assertIsNotNone(datasource.value.id)
        datasourceId = datasource.value.id

        # Create Manual Import
        importResult = datasourcesApi.create_manual_import(
            {'test': 'test import'},
            self.containerId,
            datasourceId
        )
        self.assertIsNotNone(importResult.value)

        pass


if __name__ == '__main__':
    unittest.main()
