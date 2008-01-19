__version__ = '1.0a2'

from setuptools import setup, find_packages
import sys, os
import textwrap


setup(
    name="SchevoSql",

    version=__version__,

    description="Schevo tools for SQL databases",

    long_description=textwrap.dedent("""
    Provides export from Schevo_ databases to SQL databases.

    .. _Schevo: http://schevo.org/

    You can also get the `latest development version
    <http://getschevo.org/hg/repos.cgi/schevosql-dev/archive/tip.tar.gz#egg=SchevoSql-dev>`__.
    """),

    classifiers=[
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Database :: Database Engines/Servers',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],

    keywords='',

    author='Orbtech, L.L.C. and contributors',
    author_email='schevo@googlegroups.com',

    url='http://schevo.org/wiki/SchevoSql',

    license='LGPL',

    platforms=['UNIX', 'Windows'],

    packages=find_packages(exclude=['doc', 'tests']),

    include_package_data=True,

    zip_safe=False,

    install_requires=[
    'Schevo >= 3.0',
    'RuleDispatch == dev, >= 0.5a0dev-r2306',
    'DecoratorTools',
    ],

    tests_require=[
    'nose >= 0.10.1',
    ],
    test_suite='nose.collector',

    extras_require={
    },

    dependency_links = [
    'http://turbogears.org/download/filelist.html',
    ],

    entry_points = """
    """,
    )
