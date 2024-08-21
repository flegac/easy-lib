from setuptools import setup, find_packages

setup(
    name="easy-config",
    version="0.0.1.dev0",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    description='Config file (dataclass / json) toolkit',
    install_requires=[line for line in open('requirements.txt')],
    include_package_data=True,
)
