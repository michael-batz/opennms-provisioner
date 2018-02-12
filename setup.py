"""
opennms-provisioner setup

This is the setup of opennms-provisioner

:license: MIT, see LICENSE for more details
:copyright: (c) 2018 by Michael Batz, see AUTHORS for more details
"""
import setuptools

setuptools.setup(
    name="opennms-provisioner",
    version="1.0.0dev1",
    packages=setuptools.find_packages(),

    # meta information
    author="Michael Batz",
    url="https://github.com/michael-batz/opennms-provisioner",
    license="MIT",

    # handle non python files
    include_package_data=True,

    # requirements
    install_requires=[
        "requests>=2.0.0"
    ],

    # install scripts
    entry_points={
        "console_scripts": [
            "opennms-provisioner = provisioner.__main__:main"
        ]
    },

    # don't run egg as a zip file, to enable user access to configuration files
    zip_safe=False
)
