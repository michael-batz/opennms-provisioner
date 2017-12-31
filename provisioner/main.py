#!/usr/bin/env python3
"""
opennms-provisioner main module

This is the main module of opennms-provisioner

:license: MIT, see LICENSE for more details
:copyright: (c) 2018 by Michael Batz, see AUTHORS for more details
"""

import sys
import opennms

def main():
    """main function"""
    print("Sample Project")

    # testing
    testnode = opennms.Node("testnode.example.net", "1")
    testnode.add_interface("127.0.0.1")
    testnode.add_category("Test")
    print(testnode)


if __name__ == "__main__":
    main()
