#!/usr/bin/env python
# coding: utf-8

from distutils.core import setup
import os
import setuplib

packages, package_data = setuplib.find_packages('simpleshop')

setup(name='simpleshop',
    version=__import__('simpleshop').__version__,
    description='A very basic shop for FeinCMS',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author=u'Simon Bächler',
    author_email='sb@feinheit.ch',
    url='http://github.com/sbaechler/simpleshop/',
    license='BSD License',
    platforms=['OS Independent'],
    packages=packages,
    package_data=package_data,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
    ],
)
