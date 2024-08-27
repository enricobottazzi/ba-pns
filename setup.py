from setuptools import setup, find_packages

setup(
    name="ba-pns",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'networkx==3.1',
        'numpy==1.24.1',
        'matplotlib==3.7.2',
        'powerlaw==1.5',
        'pandas==2.2.2',
    ],
    author="Enrico Bottazzi",
)