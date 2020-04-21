from setuptools import setup

setup(name='viya-rest-py',
      version='0.1',
      description="Python wrapper to ease access to SAS Viya REST API's",
      url='http://github.com/sbxxab/funniest',
      author='Xavier Bizoux',
      author_email='xavier.bizoux@sas.com',
      license='MIT',
      packages=['viya-rest-py'],
      install_requires=[
          'requests'
      ],
      include_package_data=True,
      zip_safe=False)
