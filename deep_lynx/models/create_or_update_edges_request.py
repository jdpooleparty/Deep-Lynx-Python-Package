# coding: utf-8

"""
    DeepLynx

    The construction of megaprojects has consistently demonstrated challenges for project managers in regard to meeting cost, schedule, and performance requirements. Megaproject construction challenges are common place within megaprojects with many active projects in the United States failing to meet cost and schedule efforts by significant margins. Currently, engineering teams operate in siloed tools and disparate teams where connections across design, procurement, and construction systems are translated manually or over brittle point-to-point integrations. The manual nature of data exchange increases the risk of silent errors in the reactor design, with each silent error cascading across the design. These cascading errors lead to uncontrollable risk during construction, resulting in significant delays and cost overruns. DeepLynx allows for an integrated platform during design and operations of mega projects. The DeepLynx Core API delivers a few main features. 1. Provides a set of methods and endpoints for manipulating data in an object oriented database. This allows us to store complex datatypes as records and then to compile them into actual, modifiable objects at run-time. Users can store taxonomies or ontologies in a readable format. 2. Provides methods for storing and retrieving data in a graph database. This data is structured and validated against the aformentioned object oriented database before storage.  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class CreateOrUpdateEdgesRequest(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'container_id': 'str',
        'data_source_id': 'str',
        'origin_id': 'str',
        'destination_id': 'str',
        'origin_original_id': 'str',
        'destination_original_id': 'str',
        'relationship_pair_id': 'str',
        'origin_data_source_id': 'str',
        'destination_data_source_id': 'str',
        'destination_metatype_id': 'str',
        'origin_metatype_id': 'str',
        'properties': 'object'
    }

    attribute_map = {
        'container_id': 'container_id',
        'data_source_id': 'data_source_id',
        'origin_id': 'origin_id',
        'destination_id': 'destination_id',
        'origin_original_id': 'origin_original_id',
        'destination_original_id': 'destination_original_id',
        'relationship_pair_id': 'relationship_pair_id',
        'origin_data_source_id': 'origin_data_source_id',
        'destination_data_source_id': 'destination_data_source_id',
        'destination_metatype_id': 'destination_metatype_id',
        'origin_metatype_id': 'origin_metatype_id',
        'properties': 'properties'
    }

    def __init__(self, container_id=None, data_source_id=None, origin_id=None, destination_id=None, origin_original_id=None, destination_original_id=None, relationship_pair_id=None, origin_data_source_id=None, destination_data_source_id=None, destination_metatype_id=None, origin_metatype_id=None, properties=None):  # noqa: E501
        """CreateOrUpdateEdgesRequest - a model defined in Swagger"""  # noqa: E501
        self._container_id = None
        self._data_source_id = None
        self._origin_id = None
        self._destination_id = None
        self._origin_original_id = None
        self._destination_original_id = None
        self._relationship_pair_id = None
        self._origin_data_source_id = None
        self._destination_data_source_id = None
        self._destination_metatype_id = None
        self._origin_metatype_id = None
        self._properties = None
        self.discriminator = None
        self.container_id = container_id
        self.data_source_id = data_source_id
        self.origin_id = origin_id
        self.destination_id = destination_id
        if origin_original_id is not None:
            self.origin_original_id = origin_original_id
        if destination_original_id is not None:
            self.destination_original_id = destination_original_id
        self.relationship_pair_id = relationship_pair_id
        if origin_data_source_id is not None:
            self.origin_data_source_id = origin_data_source_id
        if destination_data_source_id is not None:
            self.destination_data_source_id = destination_data_source_id
        if destination_metatype_id is not None:
            self.destination_metatype_id = destination_metatype_id
        if origin_metatype_id is not None:
            self.origin_metatype_id = origin_metatype_id
        if properties is not None:
            self.properties = properties

    @property
    def container_id(self):
        """Gets the container_id of this CreateOrUpdateEdgesRequest.  # noqa: E501


        :return: The container_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :rtype: str
        """
        return self._container_id

    @container_id.setter
    def container_id(self, container_id):
        """Sets the container_id of this CreateOrUpdateEdgesRequest.


        :param container_id: The container_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :type: str
        """
        if container_id is None:
            raise ValueError("Invalid value for `container_id`, must not be `None`")  # noqa: E501

        self._container_id = container_id

    @property
    def data_source_id(self):
        """Gets the data_source_id of this CreateOrUpdateEdgesRequest.  # noqa: E501


        :return: The data_source_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :rtype: str
        """
        return self._data_source_id

    @data_source_id.setter
    def data_source_id(self, data_source_id):
        """Sets the data_source_id of this CreateOrUpdateEdgesRequest.


        :param data_source_id: The data_source_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :type: str
        """
        if data_source_id is None:
            raise ValueError("Invalid value for `data_source_id`, must not be `None`")  # noqa: E501

        self._data_source_id = data_source_id

    @property
    def origin_id(self):
        """Gets the origin_id of this CreateOrUpdateEdgesRequest.  # noqa: E501


        :return: The origin_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :rtype: str
        """
        return self._origin_id

    @origin_id.setter
    def origin_id(self, origin_id):
        """Sets the origin_id of this CreateOrUpdateEdgesRequest.


        :param origin_id: The origin_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :type: str
        """
        if origin_id is None:
            raise ValueError("Invalid value for `origin_id`, must not be `None`")  # noqa: E501

        self._origin_id = origin_id

    @property
    def destination_id(self):
        """Gets the destination_id of this CreateOrUpdateEdgesRequest.  # noqa: E501


        :return: The destination_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :rtype: str
        """
        return self._destination_id

    @destination_id.setter
    def destination_id(self, destination_id):
        """Sets the destination_id of this CreateOrUpdateEdgesRequest.


        :param destination_id: The destination_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :type: str
        """
        if destination_id is None:
            raise ValueError("Invalid value for `destination_id`, must not be `None`")  # noqa: E501

        self._destination_id = destination_id

    @property
    def origin_original_id(self):
        """Gets the origin_original_id of this CreateOrUpdateEdgesRequest.  # noqa: E501


        :return: The origin_original_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :rtype: str
        """
        return self._origin_original_id

    @origin_original_id.setter
    def origin_original_id(self, origin_original_id):
        """Sets the origin_original_id of this CreateOrUpdateEdgesRequest.


        :param origin_original_id: The origin_original_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :type: str
        """

        self._origin_original_id = origin_original_id

    @property
    def destination_original_id(self):
        """Gets the destination_original_id of this CreateOrUpdateEdgesRequest.  # noqa: E501


        :return: The destination_original_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :rtype: str
        """
        return self._destination_original_id

    @destination_original_id.setter
    def destination_original_id(self, destination_original_id):
        """Sets the destination_original_id of this CreateOrUpdateEdgesRequest.


        :param destination_original_id: The destination_original_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :type: str
        """

        self._destination_original_id = destination_original_id

    @property
    def relationship_pair_id(self):
        """Gets the relationship_pair_id of this CreateOrUpdateEdgesRequest.  # noqa: E501


        :return: The relationship_pair_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :rtype: str
        """
        return self._relationship_pair_id

    @relationship_pair_id.setter
    def relationship_pair_id(self, relationship_pair_id):
        """Sets the relationship_pair_id of this CreateOrUpdateEdgesRequest.


        :param relationship_pair_id: The relationship_pair_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :type: str
        """
        if relationship_pair_id is None:
            raise ValueError("Invalid value for `relationship_pair_id`, must not be `None`")  # noqa: E501

        self._relationship_pair_id = relationship_pair_id

    @property
    def origin_data_source_id(self):
        """Gets the origin_data_source_id of this CreateOrUpdateEdgesRequest.  # noqa: E501


        :return: The origin_data_source_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :rtype: str
        """
        return self._origin_data_source_id

    @origin_data_source_id.setter
    def origin_data_source_id(self, origin_data_source_id):
        """Sets the origin_data_source_id of this CreateOrUpdateEdgesRequest.


        :param origin_data_source_id: The origin_data_source_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :type: str
        """

        self._origin_data_source_id = origin_data_source_id

    @property
    def destination_data_source_id(self):
        """Gets the destination_data_source_id of this CreateOrUpdateEdgesRequest.  # noqa: E501


        :return: The destination_data_source_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :rtype: str
        """
        return self._destination_data_source_id

    @destination_data_source_id.setter
    def destination_data_source_id(self, destination_data_source_id):
        """Sets the destination_data_source_id of this CreateOrUpdateEdgesRequest.


        :param destination_data_source_id: The destination_data_source_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :type: str
        """

        self._destination_data_source_id = destination_data_source_id

    @property
    def destination_metatype_id(self):
        """Gets the destination_metatype_id of this CreateOrUpdateEdgesRequest.  # noqa: E501


        :return: The destination_metatype_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :rtype: str
        """
        return self._destination_metatype_id

    @destination_metatype_id.setter
    def destination_metatype_id(self, destination_metatype_id):
        """Sets the destination_metatype_id of this CreateOrUpdateEdgesRequest.


        :param destination_metatype_id: The destination_metatype_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :type: str
        """

        self._destination_metatype_id = destination_metatype_id

    @property
    def origin_metatype_id(self):
        """Gets the origin_metatype_id of this CreateOrUpdateEdgesRequest.  # noqa: E501


        :return: The origin_metatype_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :rtype: str
        """
        return self._origin_metatype_id

    @origin_metatype_id.setter
    def origin_metatype_id(self, origin_metatype_id):
        """Sets the origin_metatype_id of this CreateOrUpdateEdgesRequest.


        :param origin_metatype_id: The origin_metatype_id of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :type: str
        """

        self._origin_metatype_id = origin_metatype_id

    @property
    def properties(self):
        """Gets the properties of this CreateOrUpdateEdgesRequest.  # noqa: E501


        :return: The properties of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :rtype: object
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this CreateOrUpdateEdgesRequest.


        :param properties: The properties of this CreateOrUpdateEdgesRequest.  # noqa: E501
        :type: object
        """

        self._properties = properties

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(CreateOrUpdateEdgesRequest, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CreateOrUpdateEdgesRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
