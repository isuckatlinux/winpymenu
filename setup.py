from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.0.1"
DESCRIPTION = "Python cli menu for python"


setup(
    name="winpymenu",
    version=VERSION,
    author="Pedro García & Yohan Díaz",
    author_email="pedroluisgarciamontil@gmail.com",
    packages=find_packages(),
    keywords=["menu", "cli"]
)