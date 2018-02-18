###############################################################
#                                                             #
# Makefile for opennms-provisioner                            #
#                                                             #
###############################################################

# set environment variables
BIN_PYTHON=python3
BIN_SPHINX=sphinx-build
BIN_PIP=pip3
DIR_TEMP="./temp"
DIR_BUILD="./target"
DIR_WHEEL_BUILD="${DIR_BUILD}/wheel"
DIR_DOCS_SOURCE="docs/source"
DIR_DOCS_BUILD="${DIR_BUILD}/docs"

# set default variables
.DEFAULT_GOAL := wheel

# create Python wheel in target directory
.PHONY: wheel
wheel:
	${BIN_PYTHON} setup.py build --build-base ${DIR_TEMP} \
						   egg_info --egg-base ${DIR_TEMP} \
						   bdist_wheel --bdist-dir ${DIR_TEMP} --dist-dir ${DIR_WHEEL_BUILD}

# install Pyton wheel with pip
.PHONY: install
install: wheel
	${BIN_PIP} install ${DIR_WHEEL_BUILD}/*.whl


# create documentation with Sphinx
.PHONY: docs
docs:
	${BIN_SPHINX} -b html -a ${DIR_DOCS_SOURCE} ${DIR_DOCS_BUILD}

# clean target directory
.PHONY: clean
clean:
	rm -Rf ${DIR_BUILD}
