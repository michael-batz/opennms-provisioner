Plugin development
==================
To develop your own source for opennms-provisioner, please have a look at *contrib/provisioner-plugin-demosource*. It 
is an example of a very simple source.

Getting started
---------------
Start with writing your own source class, which extends *provisioner.source.Source*. Overwrite the function
*get_nodes(self)*. This method needs to return a list with *provisioner.opennms.Node* objects.

Example::

    import provisioner.source
    import provisioner.opennms

    class DemoSource(provisioner.source.Source):

        def __init__(self, name, parameters):
            provisioner.source.Source.__init__(self, name, parameters)

        def get_nodes(self):
            # list with provisioner.opennms.Node objects
            nodelist = []

            # create provisioner.opennms.Node objects
            node_1 = provisioner.opennms.Node("testnode1", "1")
            node_1.add_interface("127.0.0.1")
            node_1.add_service("127.0.0.1", "ICMP")
            node_1.add_service("127.0.0.1", "SNMP")
            node_1.add_asset("city", "Fulda")
            node_1.add_asset("zip", "36041")
            node_1.add_category("DemoSource")
            nodelist.append(node_1)

            # return nodelist
            return nodelist


Configuration options
---------------------

