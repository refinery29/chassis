"""Chassis: Opinionated REST Framework."""

from setuptools import find_packages, setup

setup(
    name='chassis',
    version='0.1.2',
    packages=find_packages(),
    description="Opinionated REST Framework",
    author="Refinery 29",
    author_email="chassis-project@refinery29.com",
    url="https://github.com/refinery29/chassis",
    download_url="https://github.com/refinery29/chassis/archive/v0.1.2.tar.gz",
    keywords=['Tornado', 'RESTful', 'REST', 'API', 'JSON', 'framework'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
    install_requires=[
        'tornado'
    ],
    long_description="""\
Chassis is Refinery29's framework layer on top of Tornado for rapidly
building performant, self-documenting JSON-based REST APIs.
"""
    )

# TODO: Add validate-email==1.3 dependency
