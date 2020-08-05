from setuptools import setup, find_packages

setup(name='pyfdam',
      version='0.1',
      description='Code for fitting impedance data and simulating discharge experiments',
      url='http://github.com/muhammadhasyim/pyfdam',
      author='Muhammad R. Hasyim',
      author_email='muhammad_hasyim@berkeley.edu',
      license='MIT',
      packages=find_packages(),
      install_requires=['numpy','scipy','lmfit'],
      zip_safe=False)
