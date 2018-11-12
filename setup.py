from setuptools import setup, find_packages

setup(
    name = 'markbook',
    version = '0.0.1',
    description = 'Work in the notebook, collaborate in markdown',
    packages = find_packages(),
    install_requires = ['nbformat>=4'],
    url = 'https://github.com/poplarShift/markbook',
    author = 'Achim Randelhoff',
)
