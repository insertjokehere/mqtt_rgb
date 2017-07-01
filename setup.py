# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    install_reqs = f.read()


setup(
    name='mqtt_rgb',
    version='0.0.1',
    description='MQTT-to-Unicorn bridge',
    long_description=readme,
    author='Will Hughes',
    url='https://github.com/insertjokehere/mqtt_rgb',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=install_reqs
)
