
from setuptools import setup


setup(
    name='pyMSVC',
    version='0.5.3',
    url='https://github.com/kdschlosser/python_msvc',
    packages=['pyMSVC'],
    author='Kevin Schlosser',
    description='Simple to use MSVC build environment setup tool.',
    long_description=(
        'Distutils and setup tools not working properly to compile on Windows?\n'
        'Tired of having a new visual studio version break your setup program?\n'
        'This library is the solution.'
    ),
    install_requires=[
        'comtypes==1.1.11',
    ],
    license='MIT',
)
