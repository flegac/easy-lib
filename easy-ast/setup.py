from setuptools import setup, find_packages

setup(
    name="py-analyzer",
    version="0.0.1.dev0",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    description='Python AST Analyzer',
    install_requires=[line for line in open('requirements.txt')],
    include_package_data=True,
)
