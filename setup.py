# Copyright 2020 Joe H. Rahme <joehakimrahme@gmail.com>
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""A text-based dungeon crawler
"""

from setuptools import find_packages
from setuptools import setup

repo_url = "http://github.com/joehakimrahme/dungeoncrawler"

setup(
    name='DungeonCrawler',
    author="Joe H. Rahme",
    author_email="joehakimrahme@gmail.com",
    version='0.0.1',
    description="A text-based dungeon crawler",
    url=repo_url,
    download_url=repo_url + "/tarball/0.0.1",
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],

    entry_points={
        'console_scripts': [
            'dcbattle = dungeoncrawler.main:main',
        ]
    }
)
