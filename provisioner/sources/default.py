"""
opennms-provisioner default source module

This is the default source module of opennms-provisioner, which
defines several sources for getting OpenNMS nodes.

:license: MIT, see LICENSE for more details
:copyright: (c) 2018 by Michael Batz, see AUTHORS for more details
"""
import csv
import pyVim
import pyVim.connect
import pyVmomi
import source
import opennms

class CsvSource(source.Source):
    """ Source for getting VMs from a CSV file.

    This source creates OpenNMS nodes from a CSV file.

    Attributes:
        name: name of the source
        parameters: dictionary with parameters for this source
    """

    def __init__(self, name, parameters):
        source.Source.__init__(self, name, parameters)

    def get_nodes(self):
        #create nodelist
        nodelist = []

        # get parameters from config
        csv_filename = self.get_parameter("csv_filename", None)
        csv_delimiter = self.get_parameter("csv_delimiter", ";")
        csv_quotechar = self.get_parameter("csv_qoutechar", "\"")
        if not csv_filename:
            raise source.SourceException("CsvSource: csv filename not configured. Please check your configuration")

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
                node = opennms.Node(node_label, node_foreignid, node_location)

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


class VmwareSource(source.Source):
    """ Source for getting VMs from a VmWare ESX host.

    This source creates OpenNMS nodes from a VmWare ESX host.

    Attributes:
        name: name of the source
        parameters: dictionary with parameters for this source
    """

    def __init__(self, name, parameters):
        source.Source.__init__(self, name, parameters)

    def get_nodes(self):
        # create nodelist
        nodelist = []

        # get parameters from config
        vmware_host = self.get_parameter("vmware_host", "localhost")
        vmware_port = self.get_parameter("vmware_port", "443")
        vmware_user = self.get_parameter("vmware_user", "admin")
        vmware_password = self.get_parameter("vmware_password", "admin")

        # connect to Vmware server
        try:
            vmware_serviceinstance = pyVim.connect.SmartConnectNoSSL(host=vmware_host,
                                                                     user=vmware_user,
                                                                     pwd=vmware_password,
                                                                     port=int(vmware_port))
        except pyVmomi.vim.fault.InvalidLogin:
            raise source.SourceException("Vmware API: invalid login")
        except TimeoutError:
            raise source.SourceException("Vmware API: timeout connecting to API")

        # get rootFolder
        vmware_content = vmware_serviceinstance.RetrieveContent()
        vmware_folder = vmware_content.rootFolder

        # walk through entries in rootFolder
        vmware_view_type = [pyVmomi.vim.VirtualMachine]
        vmware_view_recursive = True
        vmware_view = vmware_content.viewManager.CreateContainerView(vmware_folder, vmware_view_type,
                                                                     vmware_view_recursive)

        # create node for every vm
        for vm in vmware_view.view:
            vm_hostname = vm.summary.config.name
            vm_ip = vm.summary.guest.ipAddress
            if vm_ip is not None:
                node = opennms.Node(vm_hostname, vm_hostname)
                node.add_interface(vm_ip)
                nodelist.append(node)
            else:
                self._logger.warning("VmwareSource: could not import VM %s with IP 'None'", vm_hostname)

        # close connection
        pyVim.connect.Disconnect(vmware_serviceinstance)

        # return nodelist
        return nodelist
