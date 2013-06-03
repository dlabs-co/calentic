#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from distutils.command.install import INSTALL_SCHEMES
import os

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

data_files = []

for dirpath, dirnames, filenames in os.walk('calentic'):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    if filenames:
        data_files.append(
            [dirpath, [os.path.join(dirpath, f) for f in filenames]])

setup(name='Calentic',
      version='0.0.1',
      description='Calendario TIC Aragón',
      url='http://www.calenti.co',
      download_url='http://github.com/Dlabs-co/calentic',
      license='GPL2',
      requires=['flask', 'flask_pymongo'],
      classifiers=[
          'Development Status :: 4 - Beta',
      ],
      long_description="Calendario TIC Aragón",
      packages=['calentic'],
      data_files=data_files,
      package_data={
          'calentic': [
              'static/'
              'templates/'
          ]
      },
      entry_points="""
        [console_scripts]
        calentic = calentic.server:server
        calentic_scrappery = calentic.scrappery:main
      """
    )
