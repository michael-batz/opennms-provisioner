#!/usr/bin/env python3
"""
opennms-provisioner main module

This is the main module of opennms-provisioner

:license: MIT, see LICENSE for more details
:copyright: (c) 2018 by Michael Batz, see AUTHORS for more details
"""
import argparse
import os
import sys
import logging
import logging.config
import config
import executor

def main():
    """main function"""

    # get basedir
    basedir = os.path.dirname(__file__)

    # get config and JobUtilty
    appconfig = config.AppConfig(basedir + "/../etc/appconfig.conf")
    jobutil = executor.JobUtility(appconfig)

    # get logging
    logging.basedir = basedir + "/../logs"
    logging.config.fileConfig(basedir + "/../etc/logging.conf")
    logger = logging.getLogger("app")

    # parse arguments
    parser =  argparse.ArgumentParser(description="Helper for OpenNMS Provisioning")
    parser.add_argument("jobname", help="name of the provisioning job")
    args = parser.parse_args()

    # get job
    try:
        job = jobutil.create_job(args.jobname)
        job.execute()
    except executor.ConfigException as e:
        logger.error("Configuration Error: %s", e)
        sys.exit(-1)
    except executor.SourceException as e:
        logger.error("Source Error: %s", e)
        sys.exit(-1)
    except executor.TargetException as e:
        logger.error("Target Error: %s", e)
        sys.exit(-1)


if __name__ == "__main__":
    main()
