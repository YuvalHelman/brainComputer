from setuptools import setup, find_packages


setup(
    name = 'SystemsDesignProject',
    version = '0.1.0',
    author = 'Yuval Helman',
    description = 'An example project for the Advanced-System-Design course in TAU.',
    packages = find_packages(),
    install_requires = ['click', 'flask'],
    tests_require = ['pytest', 'pytest-cov'],
)
