"""
opennms-provisioner custom source module

This module is the place for the implementation of custom sources
which are not part of opennms-provisioner. Simply inherit from
class source.Source. Please see DummySource for an example

:license: MIT, see LICENSE for more details
:copyright: (c) 2018 by Michael Batz, see AUTHORS for more details
"""
import provisioner.source
import provisioner.opennms

class DummySource(provisioner.source.Source):
    """ Dummy source.

    This is source is a test and demonstrates the implementation
    of an own source. It exports two test nodes.

    Attributes:
        name: name of the source
        parameters: dictionary with parameters for this source
    """

    def __init__(self, name, parameters):
        provisioner.source.Source.__init__(self, name, parameters)

    def get_nodes(self):
        # create nodelist
        nodelist = []

        # get parameters from config
        cat1 = self.get_parameter("cat1", None)
        cat2 = self.get_parameter("cat2", None)

        # create testnode 1
        node_1 = provisioner.opennms.Node("testnode1", "1")
        node_1.add_interface("127.0.0.1")
        node_1.add_service("127.0.0.1", "ICMP")
        node_1.add_service("127.0.0.1", "SNMP")
        node_1.add_asset("city", "Fulda")
        node_1.add_asset("zip", "36041")
        node_1.add_category("Test")
        if cat1:
            node_1.add_category(cat1)
        if cat2:
            node_1.add_category(cat2)

        # create testnode2
        node_2 = provisioner.opennms.Node("testnode2", "2")
        node_2.add_interface("127.0.0.1")
        node_2.add_asset("city", "Fulda")
        node_2.add_asset("zip", "36041")
        node_2.add_category("Test")
        if cat1:
            node_2.add_category(cat1)
        if cat2:
            node_2.add_category(cat2)

        # add nodes to list and return nodelist
        nodelist.append(node_1)
        nodelist.append(node_2)
        return nodelist
