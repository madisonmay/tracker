from setuptools import setup, find_packages

setup(
    name="tracker",
    version="0.1.1",
    author="Madison May, Chris Lee",
    author_email="madison@indico.io",
    packages=find_packages(),
    description="""
        Track the history of python object state to hunt down elusive bugs.
    """,
    license="MIT License (See LICENSE)",
    url="https://github.com/madisonmay/tracker"
)