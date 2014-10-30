# -*- coding: utf-8 -*-
#
#  droplet
#  Copyright (C) 2014 Carlos Pérez-Aradros Herce <exekias@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import pwd
import pkg_resources
import warnings


DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2rca$gbfiz)6lqc!z5jv5xs5!@9b@x%+ppoa^46bz(^vw)#%oa'

try:
    DROPLET_USER = 'droplet'
    pwd.getpwnam(DROPLET_USER)
except:
    warnings.warn("droplet user doesn't exists,"
                  "using current user", UserWarning)
    DROPLET_USER = pwd.getpwuid(os.getuid())[0]

DROPLET_HOME = pwd.getpwnam(DROPLET_USER).pw_dir


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DROPLET_HOME, 'db.sqlite'),
    },
    'volatile': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/dev/shm/%s.sqlite' % DROPLET_USER,
    }
}

DATABASE_ROUTERS = ['droplet.database.VolatileRouter', ]

ALLOWED_HOSTS = []

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Media folder
MEDIA_ROOT = ''
MEDIA_URL = ''

# Static folders
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)

ROOT_URLCONF = 'droplet.web.urls'

WSGI_APPLICATION = 'droplet.web.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'achilles',
    'django_forms_bootstrap',
    'droplet',
    'droplet.web',
    'droplet.core',
] + [app.module_name for app in pkg_resources.iter_entry_points('droplet.app')]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(levelname)s] %(module)s - %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.FileHandler',
            'filename': os.path.join(DROPLET_HOME, 'droplet.log'),
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['null'],
            'propagate': False,
            'level': 'DEBUG',
        },
    }
}
