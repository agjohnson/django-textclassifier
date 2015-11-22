import os.path
from setuptools import setup, find_packages


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    long_description = readme.read()


setup(
    name='django-textclassifier',
    version="1.0",
    package_dir={'textclassifier': 'textclassifier'},
    packages=['textclassifier'],
    description='Django text classifier validation',
    author='Anthony Johnson',
    author_email='aj@ohess.org',
    license='MIT License',
    url='http://github.com/agjohnson/django-textclassifier/',
    long_description=long_description,
    platforms=["any"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Environment :: Web Environment',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools',
                      'django',
                      'nltk',
                      'textblob'],
    tests_require=['mock'],
)
