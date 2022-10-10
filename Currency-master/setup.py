#!/bin/env python

"""
A simple currency module to:
* Retrive various info about currency
* Format currency price
* Convert between currencies
"""

import os

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

def get_readme():
	""" get README.rst content """
	with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r') as file:
		return file.read()

setup(
		name='nh-currency',
		description='A python library to convert currency, prettify price and get various currency info',
		long_description=get_readme(),
		packages=['currency'],
		install_requires=['requests'],
		version='1.0.2',
		author='Near Huscarl',
		author_email='near.huscarl@gmail.com',
		url='https://github.com/NearHuscarl/py-currency',
		license='BSD 3 Clauses',
		keywords='currency money financial',
		python_requires='>=3',
		classifiers=[
			'Development Status :: 4 - Beta',
			'Intended Audience :: Developers',
			'Topic :: Software Development :: Libraries',
			'License :: OSI Approved :: BSD License',
			'Programming Language :: Python :: 3',
			'Programming Language :: Python :: 3.2',
			'Programming Language :: Python :: 3.3',
			'Programming Language :: Python :: 3.4',
			'Programming Language :: Python :: 3.5',
			'Programming Language :: Python :: 3.6',
			],
		)
