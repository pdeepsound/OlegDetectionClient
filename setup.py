import setuptools
from os.path import join, dirname

version = "0.0.1"

with open(join(dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as fin:
    requirements = fin.read().splitlines()

setuptools.setup(
    name='od_client',
    version=version,
    license="Apache License Version 2.0",
    author="DeepSound AI",
    python_requires=">=3.7",
    description='Oleg Detection Python API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requirements,
)