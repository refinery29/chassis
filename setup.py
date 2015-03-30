from distutils.core import setup

setup(
    name='chassis',
    version='0.0.5',
    packages=['chassis'],
    description="Tornado framework for self-documenting JSON RESTful APIs.",
    author="Refinery 29",
    author_email="chassis-project@refinery29.com",
    url="https://github.com/refinery29/chassis",
    download_url="https://github.com/refinery29/chassis/archive/v0.0.5.tar.gz",
    keywords=['Tornado', 'RESTful', 'REST', 'API', 'JSON', 'framework'],
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
    long_description = """\
Chassis is Refinery29's framework layer on top of Tornado for rapidly building performant, self-documenting JSON-based REST APIs.
"""
    )
