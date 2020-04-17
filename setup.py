from setuptools import setup

setup(name='SASDEVOPSPY',
      version='0.1',
      description='Python wrapper to ease the DevOps process for SAS Viya',
      url='http://github.com/sbxxab/funniest',
      author='Xavier Bizoux',
      author_email='xavier.bizoux@sas.com',
      license='MIT',
      packages=['SASDEVOPSPY'],
      install_requires=[
          'requests'
      ],
      include_package_data=True,
      zip_safe=False)
