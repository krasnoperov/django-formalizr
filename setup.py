import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(name='django-formalizr',
      version='1',
      packages=['formalizr'],
      include_package_data=True,
      license='BSD License',
      description='Django AJAX Class Based Views',
      long_description=README,
      url='https://github.com/krasnoperov/django-formalizr',
      author='Aleksei Krasnoperov',
      author_email='aleksei@krasnoperov.me',
      test_suite="runtests.runtests",
      install_requires=[
          'django',
      ],
      classifiers=[
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      zip_safe=False)
