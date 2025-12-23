from setuptools import setup


version = "1.0.0.dev0"

long_description = open("README.rst").read() + "\n" + open("CHANGES.rst").read() + "\n"

setup(
    name="plone.jsonserializer",
    version=version,
    description="JSON serialization/deserialization adapters for Plone.",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.2",
        "Framework :: Plone :: Addon",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="plone json serializer",
    author="Plone Foundation",
    author_email="foundation@plone.org",
    url="https://github.com/plone/plone.jsonserializer/",
    license="gpl",
    include_package_data=True,
    python_requires=">=3.10",
    zip_safe=False,
    install_requires=[
        "setuptools",
    ],
    extras_require={
        "test": [
            "plone.app.testing >= 4.2.2",
        ]
    },
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
