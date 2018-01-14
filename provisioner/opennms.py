"""
opennms-provisioner opennms module

This module defines OpenNMS nodes, requisitions and targets and
is responsible for communicating with OpenNMS.

:license: MIT, see LICENSE for more details
:copyright: (c) 2018 by Michael Batz, see AUTHORS for more details
"""
import xml.etree.ElementTree as ET
import xml.dom.minidom
import requests

class Node(object):
    """ An OpenNMS node object.

    This class represents an OpenNMS node that should be created
    in a requisition.

    Attributes:
        label: label of the node
        foreign_id: foreign ID of the node
        location: (minion) location of the node or None
    """

    def __init__(self, label, foreign_id, location=None):
        """ inits a node """
        self.__label = label
        self.__foreign_id = foreign_id
        self.__location = location
        self.__iface_service_map = {}
        self.__categories = set()
        self.__assets = {}

    def get_foreign_id(self):
        """ returns the foreign_id """
        return self.__foreign_id

    def add_interface(self, ip):
        """ adds a new IP interface """
        if ip not in self.__iface_service_map:
            self.__iface_service_map[ip] = set()

    def add_service(self, ip, service):
        """ adds a new service to the node """
        # add interface
        self.add_interface(ip)
        # add service
        self.__iface_service_map[ip].add(service)

    def add_category(self, category):
        """ adds a new category """
        self.__categories.add(category)

    def add_asset(self, key, value):
        """ adds an asset record """
        self.__assets[key] = value

    def get_xml_element(self):
        """ returns the OpenNMS node as XML element """
        # node element
        attributes = {}
        attributes["foreign-id"] = self.__foreign_id
        attributes["node-label"] = self.__label
        if self.__location:
            attributes["location"] = self.__location
        node = ET.Element("node", attributes)

        # interfaces
        for interface in self.__iface_service_map:
            attributes = {}
            attributes["ip-addr"] = interface
            iface = ET.SubElement(node, "interface", attributes)
            for service in self.__iface_service_map[interface]:
                subattributes = {}
                subattributes["service-name"] = service
                ET.SubElement(iface, "monitored-service", subattributes)

        # categories
        for category in self.__categories:
            attributes = {}
            attributes["name"] = category
            ET.SubElement(node, "category", attributes)

        # assets
        for asset in self.__assets:
            attributes = {}
            attributes["name"] = asset
            attributes["value"] = self.__assets[asset]
            ET.SubElement(node, "asset", attributes)

        # return xml
        return node

    def get_xml_string(self):
        """ returns the OpenNMS node as XML string """
        element = self.get_xml_element()
        return ET.tostring(element, encoding="unicode", method="xml")

    def __repr__(self):
        output = "Node " + self.__label
        return output


class Requisition(object):
    """ An OpenNMS requisition object.

    This class represents an OpenNMS requisition.

    Attributes:
        name: name of the requisition
    """
    def __init__(self, name):
        self.__name = name
        self.__nodes = {}

    def add_node(self, node):
        """ Add an OpenNMS node to the requisition """
        if not isinstance(node, Node):
            raise Exception("not a Node object")
        self.__nodes[node.get_foreign_id()] = node

    def add_nodelist(self, nodelist):
        """ Add a list of OpenNMS nodes to the requisition """
        for node in nodelist:
            self.add_node(node)

    def get_xml_string(self):
        """ return the requisition as XML string """
        # requisition object
        attributes = {}
        attributes["foreign-source"] = self.__name
        requisition = ET.Element("model-import", attributes)

        # add nodes
        for foreign_id in self.__nodes:
            requisition.append(self.__nodes[foreign_id].get_xml_element())

        # return XML string
        return ET.tostring(requisition, encoding="unicode", method="xml")


class Target(object):
    """ An OpenNMS target object.

    This class represents an OpenNMS target.

    Attributes:
        name: name of the target
        rest_url: URL of the OpenNMS REST API
        rest_user: username for the OpenNMS REST API
        rest_password: password for the OpenNMS REST API
        requisition_name: name of the requisition to export nodes
    """
    def __init__(self, name, rest_url, rest_user, rest_password, requisition_name):
        """ create a new OpenNMS target """
        self.__name = name
        self.__rest_url = rest_url
        self.__rest_user = rest_user
        self.__rest_password = rest_password
        self.__requisition_name = requisition_name

    def create_requisition(self, nodelist, simulation):
        """ create and export the requisition

        Parameters:
            nodelist: list with OpenNMS node objects to export
            simulation: only print the requisition as XML, do not export them to OpenNMS
        """
        # create requisition
        requisition = Requisition(self.__requisition_name)
        requisition.add_nodelist(nodelist)

        if simulation:
            # pretty print
            requisition_dom = xml.dom.minidom.parseString(requisition.get_xml_string())
            print(requisition_dom.toprettyxml())

        else:
            # export requisition
            xmldata = requisition.get_xml_string()
            url = self.__rest_url + "/requisitions"
            request_header = {
                "Content-Type": "application/xml"
            }
            try:
                response = requests.post(url, data=xmldata, headers=request_header,
                                         auth=(self.__rest_user, self.__rest_password), verify=False)
                if response.status_code > 202:
                    error_message = "Error sending data to OpenNMS REST API /requisitions. HTTP/{}"
                    error_message.format(response.status_code,)
                    raise ConnectionException(error_message)
            except requests.exceptions.ConnectionError:
                raise ConnectionException("Error connecting to OpenNMS REST API")

            # synchronize
            url = self.__rest_url + "/requisitions/" + self.__requisition_name + "/import"
            try:
                response = requests.put(url, data="", auth=(self.__rest_user, self.__rest_password), verify=False)
                if response.status_code > 202:
                    error_message = "Error sending data to OpenNMS REST API /requisitions/<req>/import. HTTP/{}"
                    error_message.format(response.status_code,)
                    raise Exception(error_message)
            except requests.exceptions.ConnectionError:
                raise ConnectionException("Error connecting to OpenNMS REST API")


class ConnectionException(Exception):
    """ ConnectionException.

    Exception to be raised, if there are problems communicating
    to the OpenNMS REST API.
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
