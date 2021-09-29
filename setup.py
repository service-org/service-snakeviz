#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from pathlib import Path
from setuptools import setup, find_packages

readme = Path.cwd().joinpath('LETSGO.md').open().read()

setup(
    version='0.0.1',
    name='service-snakeviz',
    author='forcemain@163.com',
    url='https://github.com/service-org/',
    license='Apache License, Version 2.0',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['test', 'test.*']),
    package_data={'service_snakeviz': [
        'core/middlewares/snakeviz/static/*.ico',
        'core/middlewares/snakeviz/static/*.js',
        'core/middlewares/snakeviz/static/*.css',
        'core/middlewares/snakeviz/static/vendor/*.js',
        'core/middlewares/snakeviz/static/vendor/*.css',
        'core/middlewares/snakeviz/static/images/*.png',
        'core/middlewares/snakeviz/templates/*.html'
    ]},
    classifiers=[
        'Typing :: Typed',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=['service-webserver', 'jinja2==3.0.1']
)
