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

class RSACancelRequest(object):
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
        'authn_attempt_id': 'str',
        'remove_attempt_id': 'bool'
    }

    attribute_map = {
        'authn_attempt_id': 'authnAttemptId',
        'remove_attempt_id': 'removeAttemptId'
    }

    def __init__(self, authn_attempt_id=None, remove_attempt_id=None):  # noqa: E501
        """RSACancelRequest - a model defined in Swagger"""  # noqa: E501
        self._authn_attempt_id = None
        self._remove_attempt_id = None
        self.discriminator = None
        self.authn_attempt_id = authn_attempt_id
        if remove_attempt_id is not None:
            self.remove_attempt_id = remove_attempt_id

    @property
    def authn_attempt_id(self):
        """Gets the authn_attempt_id of this RSACancelRequest.  # noqa: E501


        :return: The authn_attempt_id of this RSACancelRequest.  # noqa: E501
        :rtype: str
        """
        return self._authn_attempt_id

    @authn_attempt_id.setter
    def authn_attempt_id(self, authn_attempt_id):
        """Sets the authn_attempt_id of this RSACancelRequest.


        :param authn_attempt_id: The authn_attempt_id of this RSACancelRequest.  # noqa: E501
        :type: str
        """
        if authn_attempt_id is None:
            raise ValueError("Invalid value for `authn_attempt_id`, must not be `None`")  # noqa: E501

        self._authn_attempt_id = authn_attempt_id

    @property
    def remove_attempt_id(self):
        """Gets the remove_attempt_id of this RSACancelRequest.  # noqa: E501


        :return: The remove_attempt_id of this RSACancelRequest.  # noqa: E501
        :rtype: bool
        """
        return self._remove_attempt_id

    @remove_attempt_id.setter
    def remove_attempt_id(self, remove_attempt_id):
        """Sets the remove_attempt_id of this RSACancelRequest.


        :param remove_attempt_id: The remove_attempt_id of this RSACancelRequest.  # noqa: E501
        :type: bool
        """

        self._remove_attempt_id = remove_attempt_id

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
        if issubclass(RSACancelRequest, dict):
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
        if not isinstance(other, RSACancelRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
