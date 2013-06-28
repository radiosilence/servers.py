# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages


requires = []
dep_links = []

for dep in open('requirements.txt').read().split("\n"):
    if dep.startswith('git+'):
        dep_links.append(dep)
    else:
        requires.append(dep)


setup(
    name="servers.py",
    version="0.1.7",
    description="Config generation library.",
    author=u"James Cleveland",
    author_email="james@dapperdogstudios.com",
    url="https://github.com/radiosilence/servers.py",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    dependency_links=dep_links,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        ],
    zip_safe=False,
)
