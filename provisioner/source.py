"""
opennms-provisioner source module

This is the source module of opennms-provisioner, which defines
abstract classes and excpetions to implement your own source.

:license: MIT, see LICENSE for more details
:copyright: (c) 2018 by Michael Batz, see AUTHORS for more details
"""
import logging

class Source(object):
    """ Abstract source for getting OpenNMS nodes.

    This is an abstract source class. To implement your own
    source, inherit from this class and implement the method
    get_nodelist().

    Attributes:
        name: name of the source
        parameters: dictionary with parameters for this source
    """

    def __init__(self, name, parameters):
        """ create a new instance """
        self._name = name
        self._parameters = parameters
        self._logger = logging.getLogger("app")

    def get_parameter(self, name, default=None):
        """ Get a source parameter.

        Return the value of the source parameter name, or use
        default, if the parameter does not exist.

        Parameters:
            name: name of the parameter
            default: default value to use, if the parameter
                does not exist
        """
        output = default
        if name in self._parameters:
            output = self._parameters[name]
        return output

    def get_nodes(self):
        """ Return a list with OpenNMS node objects.

        This methods needs to be implemented by a source and
        returns a list of opennms.Node objects.
        """
        raise Exception("not implemented")


class SourceException(Exception):
    """ SourceException.

    Exception to be raised, if there are any problems with handling
    the sources.
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
