#!/usr/bin/env python

from setuptools import setup, find_packages
import re, io

# setup.py shall not import main package
__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',  # It excludes inline comment too
    io.open('authcli/__init__.py', encoding='utf_8_sig').read()
    ).group(1)

long_description = open('README.md').read()

setup(
    name='authcli',
    version=__version__,
    description=' '.join(
        """A framework to take care of authentication/authorization for CLI apps.
        """.split()),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    author='Ray Luo',
    author_email='rayluo.mba@gmail.com',
    url='https://github.com/rayluo/authcli',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(exclude=["tests"]),
    package_data={'': ['LICENSE']},  # Do not use data_files=[...],
        # which would cause the LICENSE being copied to /usr/local,
        # and tend to fail because of insufficient permission.
        # See https://stackoverflow.com/a/14211600/728675 for more detail
    install_requires=[
        'msal~=1.0',
        'pyqrcode~=1.2.0',
    ],
)

