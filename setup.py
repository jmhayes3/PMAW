import re

from codecs import open
from os import path

from setuptools import find_packages, setup


PACKAGE = "pmaw"
PATH = path.abspath(path.dirname(__file__))

with open(path.join(PATH, "README.md"), encoding="utf-8") as fp:
    README = fp.read()
with open(path.join(PATH, PACKAGE, "const.py"), encoding="utf-8") as fp:
    VERSION = re.search('__version__ = "([^"]+)"', fp.read()).group(1)

setup(
    name=PACKAGE,
    author="jmhayes3",
    author_email="22490346+jmhayes3@users.noreply.github.com",
    python_requires="~=3.7",
    classifiers=[
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description="Python Messari API Wrapper",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "tests.*"]),
    license="MIT License",
    version=VERSION,
)
