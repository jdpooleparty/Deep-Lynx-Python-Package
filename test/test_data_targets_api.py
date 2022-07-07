# coding: utf-8

"""
    Deep Lynx

    The construction of megaprojects has consistently demonstrated challenges for project managers in regard to meeting cost, schedule, and performance requirements. Megaproject construction challenges are common place within megaprojects with many active projects in the United States failing to meet cost and schedule efforts by significant margins. Currently, engineering teams operate in siloed tools and disparate teams where connections across design, procurement, and construction systems are translated manually or over brittle point-to-point integrations. The manual nature of data exchange increases the risk of silent errors in the reactor design, with each silent error cascading across the design. These cascading errors lead to uncontrollable risk during construction, resulting in significant delays and cost overruns. Deep Lynx allows for an integrated platform during design and operations of mega projects.  The Deep Lynx Core API delivers a few main features.  1. Provides a set of methods and endpoints for manipulating data in an object oriented database. This allows us to store complex datatypes as records and then to compile them into actual, modifiable objects at run-time. Users can store taxonomies or ontologies in a readable format.  2. Provides methods for storing and retrieving data in a graph database. This data is structured and validated against the aformentioned object oriented database before storage.  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import deep_lynx
from deep_lynx.api.data_targets_api import DataTargetsApi  # noqa: E501
from deep_lynx.rest import ApiException


class TestDataTargetsApi(unittest.TestCase):
    """DataTargetsApi unit test stubs"""

    def setUp(self):
        self.api = DataTargetsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_archive_data_target(self):
        """Test case for archive_data_target

        Archive Data Target  # noqa: E501
        """
        pass

    def test_create_data_target(self):
        """Test case for create_data_target

        Create Data Target  # noqa: E501
        """
        pass

    def test_list_dat_targets(self):
        """Test case for list_dat_targets

        List Data Targets  # noqa: E501
        """
        pass

    def test_retrieve_data_target(self):
        """Test case for retrieve_data_target

        Retrieve Data Target  # noqa: E501
        """
        pass

    def test_set_data_target_active(self):
        """Test case for set_data_target_active

        Set Data Target Active  # noqa: E501
        """
        pass

    def test_set_data_target_configuration(self):
        """Test case for set_data_target_configuration

        Set Data Target Configuration  # noqa: E501
        """
        pass

    def test_set_data_target_inactive(self):
        """Test case for set_data_target_inactive

        Set Data Target Inactive  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()