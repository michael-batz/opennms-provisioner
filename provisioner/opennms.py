import xml.etree.ElementTree as ET

class Node(object):
    """ An OpenNMS node object.

    This class represents an OpenNMS node that should be created
    in a requisition.

    Attributes:
        label: label of the node
        foreign_id: foreign ID of the node
        location: (minion) location of the node
    """

    def __init__(self, label, foreign_id, location=None):
        """ inits a node """
        self.__label = label
        self.__foreign_id = foreign_id
        self.__location = location
        self.__interfaces = set()
        self.__services = {}
        self.__categories = set()
        self.__assets = {}

    def get_foreign_id(self):
        """ returns the foreign_id """
        return self.__foreign_id

    def add_interface(self, ip):
        """ adds a new IP interface """
        self.__interfaces.add(ip)

    def add_service(self, ip, service):
        """ adds a new service to the node """
        pass

    def add_category(self, category):
        """ adds a new category """
        self.__categories.add(category)

    def add_asset(self, key, value):
        self.__assets[key] = value

    def get_xml_element(self):
        # node element
        attributes = {}
        attributes["foreign-id"] = self.__foreign_id
        attributes["node-label"] = self.__label
        if self.__location:
            attributes["location"] = self.__location
        node = ET.Element("node", attributes)

        # categories
        for category in self.__categories:
            attributes = {}
            attributes["name"] = category
            ET.SubElement(node, "category", attributes)

        # assets
        for asset in self.__assets:
            attributes = {}
            attributes["name"]= asset
            attributes["value"] = self.__assets[asset]
            ET.SubElement(node, "asset", attributes)

        # return xml
        return node

    def get_xml_string(self):
        element = self.get_xml_element()
        return ET.tostring(element, encoding="unicode", method="xml")

    def __repr__(self):
        output = "Node " + self.__label
        return output


class Requisition(object):

    def __init__(self, name):
        self.__name = name
        self.__nodes = {}

    def add_node(self, node):
        if not isinstance(node, Node):
            raise Exception("not a Node object")
        self.__nodes[node.get_foreign_id()] = node

    def get_xml_string(self):
        # requisition object
        attributes = {}
        attributes["foreign-source"] = self.__name
        requisition = ET.Element("requisition", attributes)

        # add nodes
        for foreign_id in self.__nodes:
            requisition.append(self.__nodes[foreign_id].get_xml_element())

        # return XML string
        return ET.tostring(requisition, encoding="unicode", method="xml")


class Target(object):

    def __init__(self, name, rest_url, rest_user, rest_password):
        self.__name = name
        self.__rest_url = rest_url
        self.__rest_user = rest_user
        self.__rest_password = rest_password

    def export_requisition(self, requisition):
        if not isinstance(requisition, Requisition):
            raise Exception("not a Requisition object")

        print(requisition.get_xml_string())

