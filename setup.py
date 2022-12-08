from setuptools import setup


with open("README.md", "r") as fhandler:
    readme = fhandler.read()

setup(
    name="glinblin",
    version="0.0.3",
    url="https://github.com/jansilva/glinblin",
    license="MIT License",
    author="Jan Palach",
    long_description="readme",
    long_description_content_type="text/markdown",
    author_email="palach@gmail.com",
    keywords="log, aws. elasticsearch, async, python3, Linux, logger",
    description="Implements a logger formatter in order to send it to an \
        elasticsearch repository.",
    packages=["glinblin"],
    install_requires=["boto3==1.25.4"],
)
