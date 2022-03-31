from setuptools import setup, find_packages

setup(
    name="bdex",
    version='1.0',
    packages=find_packages(include=['api']),
    author="bt3gl",
    install_requires=['python-dotenv', 'requests', 'web3'],
    entry_points={
        'console_scripts': ['bdex=api.main:run_menu']
    },
)