#!/usr/bin/env python3
"""
opennms-provisioner main module

This is the main module of opennms-provisioner

:license: MIT, see LICENSE for more details
:copyright: (c) 2018 by Michael Batz, see AUTHORS for more details
"""

import sys
import config
import executor

def main():
    """main function"""

    # get config and JobUtilty
    appconfig = config.AppConfig("../etc/appconfig.conf")
    jobutil = executor.JobUtility(appconfig)

    # get job
    job = jobutil.create_job("default")
    job.execute()


if __name__ == "__main__":
    main()
