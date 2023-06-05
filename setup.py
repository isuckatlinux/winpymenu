from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

NAME = "winpymenu"
VERSION = "0.1.1-alpha"
DESCRIPTION = "Python library for console menu in Windows"


setup(
    name=NAME,
    version=VERSION,
    author="Pedro García & Yohan Díaz",
    author_email="pedroluisgarciamontil@gmail.com, yohan.diaz5632@gmail.com",
    url="https://github.com/isuckatlinux/winpymenu",
    packages=find_packages(),
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords=["menu", "cli", "python", "windows", "console", "terminal", "interactive", "display", "text menu", "library", "selection"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Topic :: Software Development'
    ]
)