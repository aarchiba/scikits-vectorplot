#!/usr/bin/env python

descr = """Algorithms to plot vector fields. 
For the moment, it only contains the line integral convolution
algorithm."""

DISTNAME            = 'scikits-vectorplot'
DESCRIPTION         = 'Vector fields plotting algorithms.'
LONG_DESCRIPTION    = descr
MAINTAINER          = 'Anne Archibald',
MAINTAINER_EMAIL    = 'archibald@astron.nl',
URL                 = 'http://projects.scipy.org/scipy/scikits'
LICENSE             = 'BSD'
DOWNLOAD_URL        = URL
PACKAGE_NAME        = 'vectorplot'
EXTRA_INFO          = dict(
    install_requires=['numpy','cython'],
    classifiers=['Development Status :: 1 - Planning',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Science/Research',
                 'Environment :: Console',
                 'License :: OSI Approved :: BSD License',
                 'Topic :: Scientific/Engineering']
    )

import os
import sys
import subprocess

import setuptools
from numpy.distutils.core import setup
from Cython.Build import cythonize


def configuration(parent_package='', top_path=None, package_name=DISTNAME):
    if os.path.exists('MANIFEST'): os.remove('MANIFEST')

    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)

    # Avoid non-useful msg: "Ignoring attempt to set 'name' (from ... "
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_subpackage(PACKAGE_NAME)
    return config

def get_version():
    """Obtain the version number"""
    import imp
    mod = imp.load_source('version', os.path.join(PACKAGE_NAME, 'version.py'))
    return mod.__version__

# Documentation building command
try:
    from sphinx.setup_command import BuildDoc as SphinxBuildDoc
    class BuildDoc(SphinxBuildDoc):
        """Run in-place build before Sphinx doc build"""
        def run(self):
            ret = subprocess.call([sys.executable, sys.argv[0], 'build_ext', '-i'])
            if ret != 0:
                raise RuntimeError("Building Scipy failed!")
            SphinxBuildDoc.run(self)
    cmdclass = {'build_sphinx': BuildDoc}
except ImportError:
    cmdclass = {}

# Call the setup function
if __name__ == "__main__":
    setup(configuration=configuration,
          name=DISTNAME,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          license=LICENSE,
          url=URL,
          download_url=DOWNLOAD_URL,
          long_description=LONG_DESCRIPTION,
          include_package_data=True,
          zip_safe=False,
          test_suite="nose.collector",
          cmdclass=cmdclass,
          ext_modules=cythonize("vectorplot/lic_internal.pyx"),
          version=get_version(),
          **EXTRA_INFO)
