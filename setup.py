from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.4.1'
DESCRIPTION = 'An Scratch API Wrapper for scratch.mit.edu'
LONG_DESCRIPTION = DESCRIPTION

# Setting up
setup(
    name="scratchrequest",
    version=VERSION,
    author="programORdie",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=["websocket-client","requests"],
    keywords=['scratch api', 'scratchrequest', 'scratch api python', 'scratch python', 'scratch for python', 'scratch', 'scratch cloud', 'scratch cloud variables', 'scratch bot'],
    url='https://github.com/programordie2/scratchrequest',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
