from setuptools import setup, find_packages

setup(
    name='pylogger',
    version='1.0.2',
    python_requires='>=3.6, <4.0',
    packages=find_packages(),
    install_requires=[
        "loguru",
    ],
)
