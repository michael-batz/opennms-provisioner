import opennms

class Source(object):

    def __init__(self, name, parameters):
        self._name = name
        self._parameters = parameters

    def get_nodes(self):
        raise Exception("not implemented")
        pass


class DummySource(Source):

    def __init__(self, name, parameters):
        Source.__init__(self, name, parameters)

    def get_nodes(self):
        # create nodelist
        nodelist = []

        # get parameters from config
        cat1 = None
        cat2 = None
        if "cat1" in self._parameters:
            cat1 = self._parameters["cat1"]
        if "cat2" in self._parameters:
            cat2 = self._parameters["cat2"]

        # create testnode 1
        node_1 = opennms.Node("testnode1", "1")
        node_1.add_interface("127.0.0.1")
        node_1.add_asset("city", "Fulda")
        node_1.add_asset("zip", "36041")
        node_1.add_category("Test")
        if cat1:
            node_1.add_category(cat1)
        if cat2:
            node_1.add_category(cat2)

        # create testnode2
        node_2 = opennms.Node("testnode2", "2")
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
