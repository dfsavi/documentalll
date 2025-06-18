from setuptools import setup, find_packages

setup(
    name="documentalll",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "documentalll = documentalll:main",
        ],
    },
    install_requires=[
        "requests",
    ],
    author="Daniel San",
    description="Process files with Ollama and generate documentation",
)
