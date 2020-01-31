from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='url_parser',
      version='2.0.0',
      description='Parse url and get all the different parts out of it',
      url='https://github.com/AdaptedAS/url_parser',
      author='Odd Jøren Røland',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author_email='odd@adapted.no',
      license='MIT',
      packages=['url_parser'],
      platforms=['any'],
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],
      zip_safe=False
      )
