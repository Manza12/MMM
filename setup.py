from setuptools import setup, find_packages

setup(
   name='mmm',
   version='1.0',
   description='Mathematical Morphology for Music',
   author='Gonzalo Romero-García',
   author_email='tritery@hotmail.com',
   # packages=['mmm', 'mmm.pianorolls', 'mmm.spectrograms'],  # same as name
   packages=find_packages(),
   # install_requires=['numpy', 'scipy', 'matplotlib', 'networkx'],  # external packages as dependencies
)