from setuptools import setup

setup(
    name='labhelperlib',
    version='0.1.0',
    description='helper functions for my personal lab work',
    author='Derick Tseng',
    author_email='derickwtseng@berkeley.edu',
    packages=['labhelperlib', 'labhelperlib.tem', 'labhelperlib.raman'],
    install_requires=[
        'numpy>1.0, <2.0',
        'pandas',
        'scipy',
        'matplotlib',
        'ncempy',
        'pillow'
    ],
)
