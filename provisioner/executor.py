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
        job_name = "job_" + name
        target_name = "target_" + self.__config.get_value(job_name, "target", None)
        source_name = "source_" + self.__config.get_value(job_name, "source", None)

        # get target from config
        target_url = self.__config.get_value(target_name, "rest_url", "http://localhost:8980/opennms/rest")
        target_user = self.__config.get_value(target_name, "rest_user", "admin")
        target_pw = self.__config.get_value(target_name, "rest_password", "admin")
        target_requisition = self.__config.get_value(target_name, "requisition", "provisioner")
        targetobj = opennms.Target(target_name, target_url, target_user, target_pw, target_requisition)

        # get source from config
        source_type = self.__config.get_value(source_name, "type", "Source")
        source_parameters = self.__config.get_section(source_name)
        sourceobj = source.DummySource(source_name, source_parameters)

        # create job
        job = Job(job_name, sourceobj, targetobj)
        return job


class Job(object):

    def __init__(self, name, sourceobj, targetobj):
        self.__name = name
        self.__sourceobj = sourceobj
        self.__targetobj = targetobj

    def execute(self):
        # get nodelist from source
        nodelist = self.__sourceobj.get_nodes()

        # create requisition
        self.__targetobj.create_requisition(nodelist)

