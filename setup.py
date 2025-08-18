"""
Setup file to esnure necessary python version, packages and entry point user can run pip install -e . to run anywhere
https://setuptools.pypa.io/en/latest/userguide/quickstart.html
https://setuptools.pypa.io/en/latest/references/keywords.html
"""
from setuptools import find_packages, setup

def read_requirements():
    with open('requirements.txt','r') as file:
        return [line.strip() for line in file if line.strip()]


setup(
    name="apiguard-scanner",
    version="0.1.0a", # Version 0.1.0, alpha
    packages=find_packages(where="src"), # Finds all packages in python folder
    package_dir={"":"src"},
    include_package_data=True,
    # Creates a command called apiguard which will run the cli function from src.cli.main module
    entry_points={
        'console_scripts': [
            'apiguard=cli.main:cli',
        ],
    },
    author="Jonathan Scruggs",
    description="API Security Scanner",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    license="MIT",
    keywords="api security scanner openapi swagger vulnerability testing",
)