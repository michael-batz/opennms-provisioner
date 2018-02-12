Concept
=======
opennms-provisioner is a tool, which reads OpenNMS node information from one of several sources (e.g. a CSV file), 
and synchronizes that information with an OpenNMS provisioning requisition using the OpenNMS REST API. Instead of 
providing a lot of integrated sources like `PRIS <https://docs.opennms.org/pris/branches/master/pris/pris.html>`_, 
the focus of opennms-provisioner is to provide a simple Python interface, which allows to easy write your own plugin 
to get nodes the in your environment. Nevertheless, there is also a `plugin bundle <https://github.com/michael-batz/opennms-provisioner-plugins>`_ 
which provides some common needed sources.

In a configuration file, jobs, sources and targets will be configured. A target defines access to an OpenNMS system. 
A source defines a class and some class dependent parameters to get OpenNMS node information. A job is the combination 
of one source and one target. opennms-provisioner will be started with a jobname, gets all node information from the 
related source and pushes the nodes to OpenNMS system defined in the related target.
