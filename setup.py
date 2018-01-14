from setuptools import setup
from codecs import open # For a consistent encoding
from os import path
import re

here = path.dirname(__file__)

def read(*names, **kwargs):
    with open(
        path.join(here, *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='git-remote-lly',

    version=find_version('remote.py'),

    description='A decentralized git built on IPFS and Ethereum',

    url='https://github.com/tarrence/lilly',

    author='Tarrence van As',
    author_email='tarrence13@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Version Control',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='git lilly lly',

    py_modules=['remote', 'lilly'],
    packages=['utils', 'protos', 'contract'],
    include_package_data = True,

    install_requires=[
        'ipfsapi>=0.4',
        'two1>=3.10.8',
        'pycrypto>=2.6.1',
        'rlp>=0.6.0',
        'pycryptodome>=3.4.7'
    ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'git-remote-lly=remote:main',
        ],
    },
)
