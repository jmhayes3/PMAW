import re
import pkg_resources


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
    version=VERSION,
    license="MIT License",
    author="jmhayes3",
    author_email="22490346+jmhayes3@users.noreply.github.com",
    classifiers=[
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
    ],
    description="Python Messari API Wrapper",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ],
    extras_require={"dev": ["pytest"]},
)
