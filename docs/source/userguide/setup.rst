Setup
=====

requirements
------------
opennms-provisioner is written in Python3 and depends on the following python libraries:

* setuptools
* requests


install from source
-------------------
To install opennms-provisioner from source, you need to have the Python setuptools installed. Use the following command 
to install the tool::

  python3 setup.py install


After setup, you can execute the script with the following command::

  /usr/bin/opennms-provisioner <jobname>


install source plugins
----------------------
After the setup of opennms-provisioner, install your source plugin(s).
