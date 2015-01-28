from Cython.Build import cythonize

def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('vectorplot', parent_package, top_path)

    #config.add_extension("lic_internal", ["lic_internal.pyx"],
    #                     language='cython')
    #config.add_subpackage('tests')

    return config
