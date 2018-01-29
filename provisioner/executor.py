"""
opennms-provisioner executor module

This is the executor module of opennms-provisioner, which will
create jobs from configuration and executes them.

:license: MIT, see LICENSE for more details
:copyright: (c) 2018 by Michael Batz, see AUTHORS for more details
"""
import importlib
import re
import provisioner.opennms
import provisioner.source

class JobUtility(object):
    """ Utility class for handling jobs.

    This class is a helper class for job handling. It defines
    functions for getting job names and create jobs from
    configuration.

    Attributes:
        config: a config object
    """

    def __init__(self, config):
        """ create a new instance """
        self.__config = config

    def get_job_names(self):
        """ return a list with all job names defined in configuration """
        return self.__config.get_sections("job_")

    def get_source_names(self):
        """ return a list with all source names defined in configuration """
        return self.__config.get_sections("source_")

    def get_target_names(self):
        """ return a list with all target names defined in configuration """
        return self.__config.get_sections("target_")

    def create_job(self, name):
        """ create and return a Job object with the given name"""
        # get job details from config
        if name not in self.get_job_names():
            raise ConfigException("Job {} does not exist in configuration".format(name,))
        job_name = "job_" + name
        job_simulate = self.__config.get_value_boolean(job_name, "simulate_only", False)
        target_name = "target_" + self.__config.get_value(job_name, "target", None)
        source_name = "source_" + self.__config.get_value(job_name, "source", None)
        if (target_name is None) or (source_name is None):
            raise ConfigException("target and source for job {} is not defined".format(job_name,))

        # get target from config
        target_url = self.__config.get_value(target_name, "rest_url", "http://localhost:8980/opennms/rest")
        target_user = self.__config.get_value(target_name, "rest_user", "admin")
        target_pw = self.__config.get_value(target_name, "rest_password", "admin")
        target_requisition = self.__config.get_value(target_name, "requisition", "provisioner")
        targetobj = provisioner.opennms.Target(target_name, target_url, target_user, target_pw, target_requisition)

        # load source class from config
        source_classname = self.__config.get_value(source_name, "class", "Source")
        source_parameters = self.__config.get_section(source_name)
        source_class = self.__load_class(source_classname)
        sourceobj = source_class(source_name, source_parameters)

        # create job
        job = Job(job_name, job_simulate, sourceobj, targetobj)
        return job

    def __load_class(self, classname):
        """ load and return the class with the given classname """
        # extract class from module
        pattern = re.compile("(.*)\.(.*)")
        match = pattern.fullmatch(classname)
        if match is None:
            raise SourceException("Could not load source {}".format(classname,))
        module_name = match.group(1)
        class_name = match.group(2)
        loaded_module = importlib.import_module(module_name)
        loaded_class = getattr(loaded_module, class_name)
        return loaded_class


class Job(object):
    """ A opennms-provisioner job.

    This class represents a job which can be executed.

    Attributes:
        name: name of the job
        simulate: don't export data to OpenNMS, print only XML export
        sourceobj: a source.Source object
        targetobj: a opennms.Target object
    """

    def __init__(self, name, simulate, sourceobj, targetobj):
        """ create a new job """
        self.__name = name
        self.__simulate = simulate
        self.__sourceobj = sourceobj
        self.__targetobj = targetobj

    def execute(self):
        """ execute the job """
        # get nodelist from source
        try:
            nodelist = self.__sourceobj.get_nodes()
        except provisioner.source.SourceException as e:
            raise SourceException(str(e))

        # create requisition
        try:
            self.__targetobj.create_requisition(nodelist, self.__simulate)
        except provisioner.opennms.ConnectionException as e:
            raise TargetException(str(e))


class ConfigException(Exception):
    """ ConfigException.

    Exception to be raised, if there are problems loading data
    from configuration.
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class TargetException(Exception):
    """ TargetException.

    Exception to be raised, if there are problems with handling
    the job's target.
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class SourceException(Exception):
    """ SourceException.

    Exception to be raised, if there are problems with handling
    the job's source.
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
