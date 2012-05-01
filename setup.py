from setuptools import setup, find_packages

setup(name='spirrid',
      version='1.0',
      description='SPIRRID',
      author='IMB, RWTH Aachen University, ISM, Brno University of Technology',
      author_email='rchudoba@imb.rwth-aachen.de',
      url='https://github.com/simvisage/spirrid',
      #namespace_packages=['spirrid', 'etsproxy'],
      packages=find_packages(exclude=('examples', 'examples.*')),
      platforms=["Windows", "Linux", "Mac OS-X", "Unix"],
      license='BSD',
      #data_files={'': ['readme.rst']},
      #include_data_data=True,
      install_requires=[],
     )
