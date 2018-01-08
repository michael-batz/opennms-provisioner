#!/usr/bin/env python3
"""
opennms-provisioner main module

This is the main module of opennms-provisioner

:license: MIT, see LICENSE for more details
:copyright: (c) 2018 by Michael Batz, see AUTHORS for more details
"""
import argparse
import os
import config
import executor

def main():
    """main function"""

    # get config and JobUtilty
    basedir = os.path.dirname(__file__)
    appconfig = config.AppConfig(basedir + "/../etc/appconfig.conf")
    jobutil = executor.JobUtility(appconfig)

    # parse arguments
    parser =  argparse.ArgumentParser(description="Helper for OpenNMS Provisioning")
    parser.add_argument("jobname", help="name of the provisioning job")
    args = parser.parse_args()

    # get job
    job = jobutil.create_job(args.jobname)
    job.execute()


if __name__ == "__main__":
    main()
