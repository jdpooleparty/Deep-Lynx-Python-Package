# coding: utf-8

"""
    Deep Lynx

    The construction of megaprojects has consistently demonstrated challenges for project managers in regard to meeting cost, schedule, and performance requirements. Megaproject construction challenges are common place within megaprojects with many active projects in the United States failing to meet cost and schedule efforts by significant margins. Currently, engineering teams operate in siloed tools and disparate teams where connections across design, procurement, and construction systems are translated manually or over brittle point-to-point integrations. The manual nature of data exchange increases the risk of silent errors in the reactor design, with each silent error cascading across the design. These cascading errors lead to uncontrollable risk during construction, resulting in significant delays and cost overruns. Deep Lynx allows for an integrated platform during design and operations of mega projects.  The Deep Lynx Core API delivers a few main features.  1. Provides a set of methods and endpoints for manipulating data in an object oriented database. This allows us to store complex datatypes as records and then to compile them into actual, modifiable objects at run-time. Users can store taxonomies or ontologies in a readable format.  2. Provides methods for storing and retrieving data in a graph database. This data is structured and validated against the aformentioned object oriented database before storage.  # noqa: E501

    OpenAPI spec version: 1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class ImportModel(object):
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
        'errors': 'str',
        'data_source_config': 'DataSourceConfig',
        'id': 'str',
        'data_source_id': 'str',
        'import_id': 'str',
        'data': 'object',
        'inserted_at': 'str',
        'created_at': 'str',
        'shape_hash': 'str',
        'container_id': 'str'
    }

    attribute_map = {
        'errors': 'errors',
        'data_source_config': 'data_source_config',
        'id': 'id',
        'data_source_id': 'data_source_id',
        'import_id': 'import_id',
        'data': 'data',
        'inserted_at': 'inserted_at',
        'created_at': 'created_at',
        'shape_hash': 'shape_hash',
        'container_id': 'container_id'
    }

    def __init__(self, errors=None, data_source_config=None, id=None, data_source_id=None, import_id=None, data=None, inserted_at=None, created_at=None, shape_hash=None, container_id=None):  # noqa: E501
        """ImportModel - a model defined in Swagger"""  # noqa: E501
        self._errors = None
        self._data_source_config = None
        self._id = None
        self._data_source_id = None
        self._import_id = None
        self._data = None
        self._inserted_at = None
        self._created_at = None
        self._shape_hash = None
        self._container_id = None
        self.discriminator = None
        if errors is not None:
            self.errors = errors
        if data_source_config is not None:
            self.data_source_config = data_source_config
        if id is not None:
            self.id = id
        self.data_source_id = data_source_id
        self.import_id = import_id
        if data is not None:
            self.data = data
        if inserted_at is not None:
            self.inserted_at = inserted_at
        if created_at is not None:
            self.created_at = created_at
        if shape_hash is not None:
            self.shape_hash = shape_hash
        if container_id is not None:
            self.container_id = container_id

    @property
    def errors(self):
        """Gets the errors of this ImportModel.  # noqa: E501


        :return: The errors of this ImportModel.  # noqa: E501
        :rtype: str
        """
        return self._errors

    @errors.setter
    def errors(self, errors):
        """Sets the errors of this ImportModel.


        :param errors: The errors of this ImportModel.  # noqa: E501
        :type: str
        """

        self._errors = errors

    @property
    def data_source_config(self):
        """Gets the data_source_config of this ImportModel.  # noqa: E501


        :return: The data_source_config of this ImportModel.  # noqa: E501
        :rtype: DataSourceConfig
        """
        return self._data_source_config

    @data_source_config.setter
    def data_source_config(self, data_source_config):
        """Sets the data_source_config of this ImportModel.


        :param data_source_config: The data_source_config of this ImportModel.  # noqa: E501
        :type: DataSourceConfig
        """

        self._data_source_config = data_source_config

    @property
    def id(self):
        """Gets the id of this ImportModel.  # noqa: E501


        :return: The id of this ImportModel.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ImportModel.


        :param id: The id of this ImportModel.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def data_source_id(self):
        """Gets the data_source_id of this ImportModel.  # noqa: E501


        :return: The data_source_id of this ImportModel.  # noqa: E501
        :rtype: str
        """
        return self._data_source_id

    @data_source_id.setter
    def data_source_id(self, data_source_id):
        """Sets the data_source_id of this ImportModel.


        :param data_source_id: The data_source_id of this ImportModel.  # noqa: E501
        :type: str
        """
        if data_source_id is None:
            raise ValueError("Invalid value for `data_source_id`, must not be `None`")  # noqa: E501

        self._data_source_id = data_source_id

    @property
    def import_id(self):
        """Gets the import_id of this ImportModel.  # noqa: E501


        :return: The import_id of this ImportModel.  # noqa: E501
        :rtype: str
        """
        return self._import_id

    @import_id.setter
    def import_id(self, import_id):
        """Sets the import_id of this ImportModel.


        :param import_id: The import_id of this ImportModel.  # noqa: E501
        :type: str
        """
        if import_id is None:
            raise ValueError("Invalid value for `import_id`, must not be `None`")  # noqa: E501

        self._import_id = import_id

    @property
    def data(self):
        """Gets the data of this ImportModel.  # noqa: E501


        :return: The data of this ImportModel.  # noqa: E501
        :rtype: object
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this ImportModel.


        :param data: The data of this ImportModel.  # noqa: E501
        :type: object
        """

        self._data = data

    @property
    def inserted_at(self):
        """Gets the inserted_at of this ImportModel.  # noqa: E501


        :return: The inserted_at of this ImportModel.  # noqa: E501
        :rtype: str
        """
        return self._inserted_at

    @inserted_at.setter
    def inserted_at(self, inserted_at):
        """Sets the inserted_at of this ImportModel.


        :param inserted_at: The inserted_at of this ImportModel.  # noqa: E501
        :type: str
        """

        self._inserted_at = inserted_at

    @property
    def created_at(self):
        """Gets the created_at of this ImportModel.  # noqa: E501


        :return: The created_at of this ImportModel.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ImportModel.


        :param created_at: The created_at of this ImportModel.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def shape_hash(self):
        """Gets the shape_hash of this ImportModel.  # noqa: E501


        :return: The shape_hash of this ImportModel.  # noqa: E501
        :rtype: str
        """
        return self._shape_hash

    @shape_hash.setter
    def shape_hash(self, shape_hash):
        """Sets the shape_hash of this ImportModel.


        :param shape_hash: The shape_hash of this ImportModel.  # noqa: E501
        :type: str
        """

        self._shape_hash = shape_hash

    @property
    def container_id(self):
        """Gets the container_id of this ImportModel.  # noqa: E501


        :return: The container_id of this ImportModel.  # noqa: E501
        :rtype: str
        """
        return self._container_id

    @container_id.setter
    def container_id(self, container_id):
        """Sets the container_id of this ImportModel.


        :param container_id: The container_id of this ImportModel.  # noqa: E501
        :type: str
        """

        self._container_id = container_id

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
        if issubclass(ImportModel, dict):
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
        if not isinstance(other, ImportModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
