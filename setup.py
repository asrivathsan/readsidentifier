#!/usr/bin/env python
import os
from distutils.core import setup
setup(name='readsidentifier',
	description="a pipeline for BLAST based read identifications",
	version='1.0',
	author='Amrita Srivathsan',
	author_email='asrivathsan@gmail.com',
	packages=['readsidentifier',],
	scripts=['readsidentifier.py'],
	data_files=['sample_config.txt','gplv3.txt'],
	py_modules=['readsidentifier/compare_pe','readsidentifier/by_taxonomy','readsidentifier/match_GiToTaxID','readsidentifier/parse_by_ID'],
	long_description=open('README.txt').read(),
	license='GPL v3',
	url='https://github.com/asrivathsan/readsidentifier-1.0',
	)

