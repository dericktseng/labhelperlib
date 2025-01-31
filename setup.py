from setuptools import setup, find_packages

setup(
    name='labhelperlib',
    version='0.1.0',
    description='helper functions for my personal lab work',
    author='Derick Tseng',
    author_email='derickwtseng@berkeley.edu',
    packages=find_packages(),
    requires=[
        'numpy==1.26.4',
        'pandas',
        'scipy',
        'matplotlib',
        'ncempy'
    ],
)
