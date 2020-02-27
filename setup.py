from setuptools import setup, find_packages


setup(
    name = 'brainComputer',
    version = '0.1.0',
    author = 'Yuval Helman',
    description = 'A module of a centralized queue-based system based on Snapshots from users',
    packages = find_packages(),
    install_requires = ['click', 'flask', 'flake8'],
    tests_require = ['pytest', 'pytest-cov'],
)

