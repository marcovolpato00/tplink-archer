from setuptools import setup, find_packages


__version__ = '0.1.2'
__author__ = 'Marco Volpato'


with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='tplink-archer',
    version=__version__,
    author=__author__,
    description='A library to interact with TP-Link Archer routers.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/marcovolpato00/tplink-archer',
    license='MIT',
    packages=find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    install_requires=[
        'requests>=2.22.0',
        'click==7.1.2'
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'tplink-archer = tplink_archer.__main__:cli'
        ]
    }
)
