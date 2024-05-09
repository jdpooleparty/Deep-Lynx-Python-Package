# coding: utf-8

"""
    DeepLynx

    The construction of megaprojects has consistently demonstrated challenges for project managers in regard to meeting cost, schedule, and performance requirements. Megaproject construction challenges are common place within megaprojects with many active projects in the United States failing to meet cost and schedule efforts by significant margins. Currently, engineering teams operate in siloed tools and disparate teams where connections across design, procurement, and construction systems are translated manually or over brittle point-to-point integrations. The manual nature of data exchange increases the risk of silent errors in the reactor design, with each silent error cascading across the design. These cascading errors lead to uncontrollable risk during construction, resulting in significant delays and cost overruns. DeepLynx allows for an integrated platform during design and operations of mega projects. The DeepLynx Core API delivers a few main features. 1. Provides a set of methods and endpoints for manipulating data in an object oriented database. This allows us to store complex datatypes as records and then to compile them into actual, modifiable objects at run-time. Users can store taxonomies or ontologies in a readable format. 2. Provides methods for storing and retrieving data in a graph database. This data is structured and validated against the aformentioned object oriented database before storage.  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import deep_lynx
from deep_lynx.api.time_series_api import TimeSeriesApi  # noqa: E501
from deep_lynx.rest import ApiException


class TestTimeSeriesApi(unittest.TestCase):
    """TimeSeriesApi unit test stubs"""

    def setUp(self):
        self.api = TimeSeriesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_timeseries_data_source_query(self):
        """Test case for timeseries_data_source_query

        Timeseries Data Source Query  # noqa: E501
        """
        pass

    def test_timeseries_node_query(self):
        """Test case for timeseries_node_query

        Timeseries Node Query  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
