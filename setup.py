from setuptools import setup

import psnprofiles_scraper


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='psnprofiles_scraper',
    version=psnprofiles_scraper.__version__,
    description='The most complete PSNprofiles scraper made in python',
    long_description=readme(),
    url='https://github.com/robiningelbrecht/psnprofiles-scraper',
    author='Robin Ingelbrecht',
    author_email='ingebrechtrobin@gmail.com',
    license='MIT',
    packages=['psnprofiles_scraper'],
    install_requires=[
        'beautifulsoup4 ~= 4.9.3',
        'progress ~= 1.5',
        'requests ~= 2.25',
    ],
    python_requires='>=3.69',
    include_package_data=True,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.9',
    ]
)
