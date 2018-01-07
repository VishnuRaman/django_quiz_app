# DJANGO_QUIZ_APP

This is a pluggable Quiz Application. 
It requires PostgreSQL and PGAdmin3 installed.
Then in the settings.py file, edit the code to:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',

        'NAME': 'name_of_database',
        'USER': 'name_of_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': 'port_indicated_on_PGAdmin3',
    }
}
