from setuptools import setup, find_packages
from pkg_resources import require, DistributionNotFound
import os

try:
    filename = os.path.join(os.path.dirname(__file__), 'README')
    description = file(filename).read()
except:
    description = ''

# Dependency check at run time
# If PIL is not found, then it is added in the ``install_requires`` list
install_requires = []   # Empty list if PIL is found
try:
    try:
        require('PIL')
    except DistributionNotFound:
        require('Image')
except DistributionNotFound:
    install_requires = ['PIL']

version = '0.1.7a'

setup(name='cropresize2',
      version=version,
      description="crop and resize an image without doing the math yourself",
      long_description=description,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='image',
      author='Jeff Hammel, Vlad Frolov',
      author_email='k0scist@gmail.com, frolvlad@gmail.com',
      url='http://pypi.python.org/pypi/cropresize2',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      crop-resize = cropresize2:main
      """,
      )
