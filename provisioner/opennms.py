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

    def return_xml(self):
        pass

    def __repr__(self):
        output = "Node " + self.__label
        return output
