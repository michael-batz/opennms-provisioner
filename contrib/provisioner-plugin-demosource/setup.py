"""
provisioner-plugin-demosource setup

This is the setup of provisioner-plugin-demosource

:license: MIT, see LICENSE for more details
:copyright: (c) 2018 by Michael Batz, see AUTHORS for more details
"""
import setuptools

setuptools.setup(
    name="provisioner-plugin-demosource",
    version="1.0.0",
    packages=setuptools.find_packages(),

    # meta information
    author="Michael Batz",
    url="https://github.com/michael-batz/opennms-provisioner",
    license="MIT"

    # requirements
    install_requires=[
        "opennms-provisioner"
    ],
)
