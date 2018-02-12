Configuration
=============
opennms-provisioner comes with the following configuration files:

appconfig.conf
--------------
appconfig.conf is the main configuration file, where jobs, sources and targets will be defined. Please see the following 
example::

  [job_dummy]
  source = dummy
  target = default
  simulate_only = true

  [source_dummy]
  class = provisioner.sources.test.DummySource
  cat1 = demo
  cat2 = test

  [target_default]
  rest_url = http://localhost:8980/opennms/rest
  rest_user = admin
  rest_password = admin
  requisition = provisioner

jobs
""""
A job will be defined in a job_* section, started by the word "job\_" and followed by the name of the job. Each job 
consists of one source and one target has the following options:

source:
    name of the source to use (without the prefix source\_)

target:
    name of the target to use (without the prefix target\_)

simulate_only:
    If set to true, the XML output for OpenNMS will only be printed on stdout, instead of sending it to the REST API


sources
"""""""
Sources will be configured in source_* sections, started by the word "source\_", followed by the source name. Each source
consists on a class name and a class dependent set of parameters.


targets
"""""""
A target will be defined in an target_* section, started by the word "target\_" plus the target's name. A target has the
following options:

rest_url:
    URL to the OpenNMS REST API

rest_user:
    username for the OpenNMS REST API

rest_password:
    password for the OpenNMS REST API

requisition:
    name of the requisition to export the nodes.


logging.conf
------------
This file is a Python3 `standard logging configuration file <https://docs.python.org/3/library/logging.config.html#configuration-file-format>`_. 
The logger *app* will be used by opennms-provisioner. In the default settings, WARNING messages were printed to stdout 
and logged into *logs/app.log*

