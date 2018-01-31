"""
opennms-provisioner vmware source module

This module provides VmWare sources for opennms-provisioner.

:license: MIT, see LICENSE for more details
:copyright: (c) 2018 by Michael Batz, see AUTHORS for more details
"""
import pyVim
import pyVim.connect
import pyVmomi
import provisioner.source
import provisioner.opennms

class VmwareSource(provisioner.source.Source):
    """ Source for getting VMs from a VmWare ESX host.

    This source creates OpenNMS nodes from a VmWare ESX host.

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
                node = provisioner.opennms.Node(vm_hostname, vm_hostname)
                node.add_interface(vm_ip)
                nodelist.append(node)
            else:
                self._logger.warning("VmwareSource: could not import VM %s with IP 'None'", vm_hostname)

        # close connection
        pyVim.connect.Disconnect(vmware_serviceinstance)

        # return nodelist
        return nodelist
