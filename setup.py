from setuptools import setup, find_packages

setup(name='viyaRestPy',
      version='0.1',
      description="Python wrapper to ease access to SAS Viya REST API's",
      url='https://gitlab.sas.com/sbxxab/viyarestpy',
      author='Xavier Bizoux',
      author_email='xavier.bizoux@sas.com',
      license='MIT',
      packages=find_packages(include=[
                             'Authentication',
                             'Authentication.*',
                             'Folders',
                             'Folders.*',
                             'Reports',
                             'Reports.*']),
      install_requires=[
          'requests'
      ],
      include_package_data=True,
      zip_safe=False)
