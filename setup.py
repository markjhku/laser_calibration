# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()


setup(
    name='laser_calibration',
    version='0.1.0',
    description='Laser calibration exercise',
    long_description=readme,
    author='Mark Ku',
    author_email='mark.jh.ku@gmail.com',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'scipy==1.15.3',
        'numpy',
	'matplotlib'
    ]
)