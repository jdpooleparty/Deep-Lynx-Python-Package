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

class InlineResponse20010Value(object):
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
        'id': 'str',
        'container_id': 'str',
        'name': 'str',
        'changelist_id': 'str',
        'created_by': 'str',
        'created_at': 'str'
    }

    attribute_map = {
        'id': 'id',
        'container_id': 'container_id',
        'name': 'name',
        'changelist_id': 'changelist_id',
        'created_by': 'created_by',
        'created_at': 'created_at'
    }

    def __init__(self, id=None, container_id=None, name=None, changelist_id=None, created_by=None, created_at=None):  # noqa: E501
        """InlineResponse20010Value - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._container_id = None
        self._name = None
        self._changelist_id = None
        self._created_by = None
        self._created_at = None
        self.discriminator = None
        self.id = id
        self.container_id = container_id
        self.name = name
        self.changelist_id = changelist_id
        self.created_by = created_by
        self.created_at = created_at

    @property
    def id(self):
        """Gets the id of this InlineResponse20010Value.  # noqa: E501


        :return: The id of this InlineResponse20010Value.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this InlineResponse20010Value.


        :param id: The id of this InlineResponse20010Value.  # noqa: E501
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def container_id(self):
        """Gets the container_id of this InlineResponse20010Value.  # noqa: E501


        :return: The container_id of this InlineResponse20010Value.  # noqa: E501
        :rtype: str
        """
        return self._container_id

    @container_id.setter
    def container_id(self, container_id):
        """Sets the container_id of this InlineResponse20010Value.


        :param container_id: The container_id of this InlineResponse20010Value.  # noqa: E501
        :type: str
        """
        if container_id is None:
            raise ValueError("Invalid value for `container_id`, must not be `None`")  # noqa: E501

        self._container_id = container_id

    @property
    def name(self):
        """Gets the name of this InlineResponse20010Value.  # noqa: E501


        :return: The name of this InlineResponse20010Value.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this InlineResponse20010Value.


        :param name: The name of this InlineResponse20010Value.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def changelist_id(self):
        """Gets the changelist_id of this InlineResponse20010Value.  # noqa: E501


        :return: The changelist_id of this InlineResponse20010Value.  # noqa: E501
        :rtype: str
        """
        return self._changelist_id

    @changelist_id.setter
    def changelist_id(self, changelist_id):
        """Sets the changelist_id of this InlineResponse20010Value.


        :param changelist_id: The changelist_id of this InlineResponse20010Value.  # noqa: E501
        :type: str
        """
        if changelist_id is None:
            raise ValueError("Invalid value for `changelist_id`, must not be `None`")  # noqa: E501

        self._changelist_id = changelist_id

    @property
    def created_by(self):
        """Gets the created_by of this InlineResponse20010Value.  # noqa: E501


        :return: The created_by of this InlineResponse20010Value.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this InlineResponse20010Value.


        :param created_by: The created_by of this InlineResponse20010Value.  # noqa: E501
        :type: str
        """
        if created_by is None:
            raise ValueError("Invalid value for `created_by`, must not be `None`")  # noqa: E501

        self._created_by = created_by

    @property
    def created_at(self):
        """Gets the created_at of this InlineResponse20010Value.  # noqa: E501


        :return: The created_at of this InlineResponse20010Value.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this InlineResponse20010Value.


        :param created_at: The created_at of this InlineResponse20010Value.  # noqa: E501
        :type: str
        """
        if created_at is None:
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

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
        if issubclass(InlineResponse20010Value, dict):
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
        if not isinstance(other, InlineResponse20010Value):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
