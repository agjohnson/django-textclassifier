.. include:: ../README.rst

Changelog
---------

v2.0
~~~~

* Dropped TextBlob and NLTK for scikit-learn. This brings a significant speed
  increase and improvement in accuracy.
* Added admin features
* Dropped file storage for database storage
* Added field wrapper to handle setting up validator for each field

v1.0
~~~~

* Initial release, using file-backed classification and based on NLTK and
  TextBlob.
