import opennms
import source

class JobUtility(object):

    def __init__(self, config):
        self.__config = config

    def get_job_names(self):
        return self.__config.get_sections("job_")

    def get_source_names(self):
        return self.__config.get_sections("source_")

    def get_target_names(self):
        return self.__config.get_sections("target_")

    def create_job(self, name):
        # get job details from config
        if name not in self.get_job_names():
            raise ConfigException("Job {} does not exist in configuration".format(name,))
        job_name = "job_" + name
        job_simulate = self.__config.get_value_boolean(job_name, "simulate_only", False)
        target_name = "target_" + self.__config.get_value(job_name, "target", None)
        source_name = "source_" + self.__config.get_value(job_name, "source", None)
        if (target_name is None) or (source_name is None):
            raise ConfigException("target and source for job %s is not defined".format(job_name,))

        # get target from config
        target_url = self.__config.get_value(target_name, "rest_url", "http://localhost:8980/opennms/rest")
        target_user = self.__config.get_value(target_name, "rest_user", "admin")
        target_pw = self.__config.get_value(target_name, "rest_password", "admin")
        target_requisition = self.__config.get_value(target_name, "requisition", "provisioner")
        targetobj = opennms.Target(target_name, target_url, target_user, target_pw, target_requisition)

        # get source from config
        source_class = self.__config.get_value(source_name, "class", "Source")
        source_parameters = self.__config.get_section(source_name)
        sourceobj = eval("source." + source_class + "(source_name, source_parameters)")

        # create job
        job = Job(job_name, job_simulate, sourceobj, targetobj)
        return job


class Job(object):

    def __init__(self, name, simulate, sourceobj, targetobj):
        self.__name = name
        self.__simulate = simulate
        self.__sourceobj = sourceobj
        self.__targetobj = targetobj

    def execute(self):
        # get nodelist from source
        nodelist = self.__sourceobj.get_nodes()

        # create requisition
        try:
            self.__targetobj.create_requisition(nodelist, self.__simulate)
        except opennms.ConnectionException as e:
            raise TargetException(str(e))


class ConfigException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class TargetException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
