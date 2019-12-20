#!/usr/bin/env python
# Copyright (c) 2016 Jonathan M. Lange <jml@mumak.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import codecs
import os

from setuptools import find_packages, setup


readme_path = os.path.join(os.path.dirname(__file__), "README.md")
with codecs.open(readme_path, encoding='utf-8', errors='replace') as readme:
    long_description = readme.read()

classifiers = [
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
]

setup(
    name="tree-format",
    long_description=long_description,
    version="0.1.2",
    packages=find_packages(),
    author="Jonathan M. Lange",
    author_email="jml@mumak.net",
    classifiers=classifiers,
    url="http://github.com/jml/tree-format",
    extras_require={
        "dev": ["pytest>=2.7.1", "testtools>=1.8.0"],
    },
)
