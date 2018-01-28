"""
opennms-provisioner setup

This is the setup of opennms-provisioner

:license: MIT, see LICENSE for more details
:copyright: (c) 2018 by Michael Batz, see AUTHORS for more details
"""
import setuptools

setuptools.setup(
    name="opennms-provisioner",
    version="master",
    packages=setuptools.find_packages(),

    # meta information
    author="Michael Batz",
    url="https://github.com/michael-batz/opennms-provisioner",
    license="MIT",

    # handle non python files
    include_package_data=True,

    # requirements
    install_requires=[
        "requests==2.18.4",
        "pyvmomi==6.5.0.2017.5.post1"
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
