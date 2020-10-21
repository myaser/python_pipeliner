import os
from setuptools import setup


def read(fname):
    '''
    Utility function to read the README file. Used for the long_description.
    It's nice, because:
    1) we have a top level README file and
    2) it's easier to type in the README file than to put a raw string in below
    '''
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="python_pipeliner",
    version="0.5.1",
    author="Mahmoud Yaser",
    author_email="me.MahmoudYaser@gmail.com",
    description=("utility package to implement pipeline architectural pattern"),
    license="MIT",
    keywords="python pipeline",
    url="https://github.com/myaser/python_pipeliner",
    packages=['pipeline'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
    ],
)
