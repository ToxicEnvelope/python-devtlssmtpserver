#!/usr/bin/env python

from distutils.core import setup

setup(name='python-devtlssmtpserver',
      version='0.1',
      description='A smtp Server for Developers with STARTTLS Support',
      author='Thomas Spycher',
      author_email='me@tspycher.com',
      url='https://github.com/tspycher/python-devtlssmtpserver.git',
      packages=['devtlssmtpserver'],
      package_dir={'devtlssmtpserver': 'src/devtlssmtpserver'},
      download_url='https://github.com/tspycher/python-devtlssmtpserver/tarball/master'
     )