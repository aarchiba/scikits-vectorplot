#!/usr/bin/env python
import os, sys

descr = """Algorithms to plot vector fields. 
For the moment, it only contains the line integral convolution
algorithm."""

DISTNAME            = 'scikits.vectorplot'
DESCRIPTION         = 'Vector fields plotting algorithms.'
LONG_DESCRIPTION    = descr
MAINTAINER          = 'Anne Archibald',
MAINTAINER_EMAIL    = 'peridot.faceted@gmail.com',
URL                 = 'http://projects.scipy.org/scipy/scikits'
LICENSE             = 'BSD'
DOWNLOAD_URL        = URL
VERSION             = '0.1.1'

import setuptools
from numpy.distutils.core import setup

def configuration(parent_package='', top_path=None, package_name=DISTNAME):
    if os.path.exists('MANIFEST'): os.remove('MANIFEST')

    from numpy.distutils.misc_util import Configuration
    config = Configuration(package_name, parent_package, top_path,
                           version = VERSION,
                           maintainer  = MAINTAINER,
                           maintainer_email = MAINTAINER_EMAIL,
                           description = DESCRIPTION,
                           license = LICENSE,
                           url = URL,
                           download_url = DOWNLOAD_URL,
                           long_description = LONG_DESCRIPTION)

    return config

if __name__ == "__main__":
    setup(configuration = configuration,
        install_requires = 'numpy',
        namespace_packages = ['scikits'],
        packages = setuptools.find_packages(),
        include_package_data = True,
        #test_suite="tester", # for python setup.py test
        zip_safe = True, # the package can run out of an .egg file
        classifiers =
            [ 'Development Status :: 1 - Planning',
              'Environment :: Console',
              'Intended Audience :: Developers',
              'Intended Audience :: Science/Research',
              'License :: OSI Approved :: BSD License',
              'Topic :: Scientific/Engineering'])
