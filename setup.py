# If true, then the svn revision won't be used to calculate the
# revision (set to True for real releases)
RELEASE = False

__version__ = '1.0a1'

from setuptools import setup, find_packages
import sys, os
import textwrap

import finddata

setup(
    name="SchevoSql",
    
    version=__version__,
    
    description="Schevo tools for SQL databases",
    
    long_description=textwrap.dedent("""
    Provides export from Schevo_ databases to SQL databases.

    .. _Schevo: http://schevo.org/

    The latest development version is available in a `Subversion
    repository
    <http://schevo.org/svn/trunk/Sql#egg=SchevoSql-dev>`__.
    """),
    
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Lesser General Public License (LGPL)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Database :: Database Engines/Servers',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    
    keywords='',
    
    author='Orbtech, L.L.C. and contributors',
    author_email='schevo-devel@lists.schevo.org',

    url='http://schevo.org/trac/wiki/SchevoSqlMain',
    
    license='LGPL',
    
    platforms=['UNIX', 'Windows'],

    packages=find_packages(exclude=['doc', 'tests']),

    package_data=finddata.find_package_data(),

    zip_safe=False,
    
    install_requires=[
    'Schevo==dev,>=3.0b2dev-r1728',
    'RuleDispatch >= 0.5a0dev',
    ],
    
    tests_require=[
    'nose >= 0.8.7',
    ],
    test_suite='nose.collector',
    
    extras_require={
    },
    
    entry_points = """
    """,
    )
