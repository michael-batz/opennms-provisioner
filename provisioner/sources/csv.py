"""
opennms-provisioner csv source module

This module provides CSV based sources for opennms-provisioner.

:license: MIT, see LICENSE for more details
:copyright: (c) 2018 by Michael Batz, see AUTHORS for more details
"""
import csv
import provisioner.source
import provisioner.opennms

class CsvSource(provisioner.source.Source):
    """ Source for getting VMs from a CSV file.

    This source creates OpenNMS nodes from a CSV file.

    Attributes:
        name: name of the source
        parameters: dictionary with parameters for this source
    """

    def __init__(self, name, parameters):
        provisioner.source.Source.__init__(self, name, parameters)

    def get_nodes(self):
        #create nodelist
        nodelist = []

        # get parameters from config
        csv_filename = self.get_parameter("csv_filename", None)
        csv_delimiter = self.get_parameter("csv_delimiter", ";")
        csv_quotechar = self.get_parameter("csv_qoutechar", "\"")
        if not csv_filename:
            message = "CsvSource: csv filename not configured. Please check your configuration"
            raise provisioner.source.SourceException(message)

        # load csv with DictReader
        with open(csv_filename) as csv_file:
            # load each row into a dict. Use first row as fieldnames
            csv_reader = csv.DictReader(csv_file, delimiter=csv_delimiter, quotechar=csv_quotechar)
            # walk over all rows and create a node per row
            for csv_row in csv_reader:
                # min field "nodelabel" must be set
                if "nodelabel" not in csv_row:
                    self._logger.warning("CsvSource: Could not import row, because no nodelabel is set. row: %s",
                                         csv_row)
                    continue

                # create node
                node_label = csv_row["nodelabel"]
                node_location = csv_row.get("location", None)
                node_foreignid = csv_row.get("foreign_id", node_label)
                node = provisioner.opennms.Node(node_label, node_foreignid, node_location)

                # add interfaces and services
                node_interfaces = csv_row.get("interfaces", None)
                node_services = csv_row.get("services", None)
                if node_interfaces:
                    for node_interface in node_interfaces.split(","):
                        node.add_interface(node_interface)
                        if node_services:
                            for node_service in node_services.split(","):
                                node.add_service(node_interface, node_service)

                # add categories and assets
                for key in csv_row.keys():
                    # add surveillance categories
                    if key.startswith("category_"):
                        node.add_category(csv_row[key])
                    # add assets
                    if key.startswith("asset_"):
                        asset_key = key[len("asset_"):]
                        asset_value = csv_row[key]
                        node.add_asset(asset_key, asset_value)

                # add node to nodelist
                nodelist.append(node)

        # return the nodes
        return nodelist
