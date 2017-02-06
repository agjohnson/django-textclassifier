#import django

DATABASES={
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}
SECRET_KEY = 'null'

INSTALLED_APPS = [
    'textclassifier',
    'tests',
]

#django.setup()
