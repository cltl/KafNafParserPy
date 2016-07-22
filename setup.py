#!/usr/bin/env python


try:
      from setuptools import setup
except ImportError:
      from distutils.core import setup





setup(name='KafNafParserPy',
      version='1.81',
      description='Parser for KAF/NAF files in Python',
      author='Ruben Izquierdo',
      author_email='rubensanvi@gmail.com',
      url='https://github.com/cltl/KafNafParserPy',
      packages = ['KafNafParserPy','KafNafParserPy.feature_extractor'],
      install_requires = ['lxml']
      )
