"""
Django settings for arches_rdm_example_project project.
"""

import json
import os
import sys
from typing import Literal
import arches
import inspect
import semantic_version
from django.utils.translation import gettext_lazy as _
from arches.settings import *


def get_env_variable(var_name):
    msg = "Set the %s environment variable"
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = msg % var_name
        raise ImproperlyConfigured(error_msg)


def get_optional_env_variable(var_name, default=None) -> str:
    try:
        return os.environ[var_name]
    except KeyError:
        return default


SECRETS_MODE = get_optional_env_variable("SECRETS_MODE", "ENV")

APP_NAME = "arches_rdm_example_project"
APP_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
DB_NAME = APP_NAME
DB_USER = get_optional_env_variable("PGUSERNAME", "postgres")
DB_PASSWORD = get_optional_env_variable("PGPASSWORD", "postgis")
DB_HOST = get_optional_env_variable("PGHOST", "localhost")
DB_PORT = get_optional_env_variable("PGPORT", "5432")
ES_USER = get_optional_env_variable("ESUSER", "elastic")
ES_PASSWORD = get_optional_env_variable("ESPASSWORD", "E1asticSearchforArche5")
ES_HOST = get_optional_env_variable("ESHOST", "localhost")
ES_PORT = int(get_optional_env_variable("ESPORT", "9200"))
WEBPACK_DEVELOPMENT_SERVER_PORT = int(
    get_optional_env_variable("WEBPACKDEVELOPMENTSERVERPORT", "8022")
)
ES_PROTOCOL = get_optional_env_variable("ESPROTOCOL", "http")
ES_VALIDATE_CERT = get_optional_env_variable("ESVALIDATE", "True") != "False"
DEBUG = bool(get_optional_env_variable("DJANGO_DEBUG", False))
KIBANA_URL = get_optional_env_variable("KIBANA_URL", "http://localhost:5601/")
KIBANA_CONFIG_BASEPATH = get_optional_env_variable("KIBANACONFIGBASEPATH", "kibana")
RESOURCE_IMPORT_LOG = get_optional_env_variable(
    "RESOURCEIMPORTLOG", os.path.join(APP_ROOT, "logs", "resource_import.log")
)
ARCHES_LOG_PATH = get_optional_env_variable(
    "ARCHESLOGPATH", os.path.join(ROOT_DIR, "arches.log")
)

STORAGE_BACKEND = get_optional_env_variable(
    "STORAGEBACKEND", "django.core.files.storage.FileSystemStorage"
)

if STORAGE_BACKEND == "storages.backends.s3.S3Storage":
    import psutil

    STORAGE_OPTIONS = {
        "bucket_name": get_env_variable("S3BUCKETNAME"),
        "file_overwrite": get_optional_env_variable("S3FILEOVERWRITE", True),
        "signature_version": get_optional_env_variable("S3SIGNATUREVERSION", "s3v4"),
        "region": get_optional_env_variable("S3REGION", "us-west-1"),
        "max_memory_size": get_optional_env_variable(
            "S3MAXMEMORY", str(psutil.virtual_memory().available * 0.5)
        ),
    }
else:
    STORAGE_OPTIONS = {}

STORAGES = {
    "default": {
        "BACKEND": STORAGE_BACKEND,
        "OPTIONS": STORAGE_OPTIONS,
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

if SECRETS_MODE == "AWS":
    try:
        import boto3
        import json

        AWS_REGION = get_optional_env_variable("AWS_REGION", "us-west-1")
        ES_SECRET_ID = get_env_variable("ES_SECRET_ID")
        DB_SECRET_ID = get_env_variable("DB_SECRET_ID")
        client = boto3.client("secretsmanager", region_name=AWS_REGION)
        es_secret = json.loads(
            client.get_secret_value(SecretId=ES_SECRET_ID)["SecretString"]
        )
        db_secret = json.loads(
            client.get_secret_value(SecretId=DB_SECRET_ID)["SecretString"]
        )
        DB_NAME = APP_NAME
        DB_USER = db_secret["user"]
        DB_PASSWORD = db_secret["password"]
        DB_HOST = db_secret["host"]
        DB_PORT = db_secret["port"]
        ES_USER = es_secret["user"]
        ES_PASSWORD = es_secret["password"]
        ES_HOST = es_secret["host"]
    except (ModuleNotFoundError, ImportError):
        pass

APP_VERSION = semantic_version.Version(major=1, minor=0, patch=0, prerelease=("a", "0"))
MIN_ARCHES_VERSION = "7.5.0b0"
MAX_ARCHES_VERSION = "7.5.1"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        },
    },
    "handlers": {
        "file": {
            "level": "WARNING",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
            "class": "logging.FileHandler",
            "filename": ARCHES_LOG_PATH,
            "formatter": "console",
        },
        "console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "loggers": {
        "arches": {
            "handlers": ["file", "console"],
            "level": "WARNING",
            "propagate": True,
        }
    },
}

STATICFILES_DIRS = (
    os.path.join(APP_ROOT, "media", "build"),
    os.path.join(APP_ROOT, "media"),
) + STATICFILES_DIRS

WEBPACK_LOADER = {
    "DEFAULT": {
        "STATS_FILE": os.path.join(APP_ROOT, "webpack/webpack-stats.json"),
    },
}

DATATYPE_LOCATIONS.append("arches_rdm_example_project.datatypes")
FUNCTION_LOCATIONS.append("arches_rdm_example_project.functions")
ETL_MODULE_LOCATIONS.append("arches_rdm_example_project.etl_modules")
SEARCH_COMPONENT_LOCATIONS.append("arches_rdm_example_project.search_components")

LOCALE_PATHS.append(os.path.join(APP_ROOT, "locale"))

FILE_TYPE_CHECKING = False
FILE_TYPES = [
    "bmp",
    "gif",
    "jpg",
    "jpeg",
    "pdf",
    "png",
    "psd",
    "rtf",
    "tif",
    "tiff",
    "xlsx",
    "csv",
    "zip",
]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_optional_env_variable(
    "DJANGO_SECRET_KEY", "69i^0^enn7-%nww6no&e%+62($hto5vk0(#tp+ygl1!9$2_^5y"
)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ROOT_URLCONF = "arches_rdm_example_project.urls"
# Modify this line as needed for your project to connect to elasticsearch with a password that you generate
ELASTICSEARCH_HOSTS = [{"scheme": ES_PROTOCOL, "host": ES_HOST, "port": ES_PORT}]
ELASTICSEARCH_CONNECTION_OPTIONS = {"timeout": 30, "basic_auth": (ES_USER, ES_PASSWORD)}
# a prefix to append to all elasticsearch indexes, note: must be lower case
ELASTICSEARCH_PREFIX = APP_NAME

ELASTICSEARCH_CUSTOM_INDEXES = []

LOAD_DEFAULT_ONTOLOGY = False
LOAD_PACKAGE_ONTOLOGIES = True
DATABASES = {
    "default": {
        "ATOMIC_REQUESTS": False,
        "AUTOCOMMIT": True,
        "CONN_MAX_AGE": 0,
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "HOST": DB_HOST,
        "NAME": APP_NAME,
        "OPTIONS": {},
        "PASSWORD": DB_PASSWORD,
        "PORT": DB_PORT,
        "POSTGIS_TEMPLATE": "template_postgis",
        "TEST": {"CHARSET": None, "COLLATION": None, "MIRROR": None, "NAME": None},
        "TIME_ZONE": None,
        "USER": DB_USER,
    }
}


INSTALLED_APPS = (
    "webpack_loader",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "arches",
    "arches.app.models",
    "arches.management",
    "guardian",
    "captcha",
    "revproxy",
    "corsheaders",
    "oauth2_provider",
    "django_celery_results",
    "compressor",
    # "silk",
    "arches_rdm_example_project",
    "arches_rdm",
)

ARCHES_APPLICATIONS = ("arches_rdm",)

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    #'arches.app.utils.middleware.TokenMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "arches.app.utils.middleware.ModifyAuthorizationHeader",
    "oauth2_provider.middleware.OAuth2TokenMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "arches.app.utils.middleware.SetAnonymousUser",
    # "silk.middleware.SilkyMiddleware",
]

STATICFILES_DIRS = build_staticfiles_dirs(
    root_dir=ROOT_DIR,
    app_root=APP_ROOT,
    arches_applications=ARCHES_APPLICATIONS,
)

TEMPLATES = build_templates_config(
    root_dir=ROOT_DIR,
    debug=DEBUG,
    app_root=APP_ROOT,
    arches_applications=ARCHES_APPLICATIONS,
)

ALLOWED_HOSTS = get_optional_env_variable("DOMAIN_NAMES", "*").split()
SYSTEM_SETTINGS_LOCAL_PATH = os.path.join(
    APP_ROOT, "system_settings", "System_Settings.json"
)
WSGI_APPLICATION = "arches_rdm_example_project.wsgi.application"

# URL that handles the media served from MEDIA_ROOT, used for managing stored files.
# It must end in a slash if set to a non-empty value.
MEDIA_URL = "/files/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = os.path.join(APP_ROOT)

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = get_optional_env_variable("DJANGO_STATIC_ROOT", "/var/www/media/")

# when hosting Arches under a sub path set this value to the sub path eg : "/{sub_path}/"
FORCE_SCRIPT_NAME = None

DEFAULT_RESOURCE_IMPORT_USER = {"username": "admin", "userid": 1}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        },
    },
    "handlers": {
        "file": {
            "level": "WARNING",  # DEBUG, INFO, WARNING, ERROR
            "class": "logging.FileHandler",
            "filename": os.path.join(APP_ROOT, "arches.log"),
            "formatter": "console",
        },
        "console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "loggers": {
        "arches": {
            "handlers": ["file", "console"],
            "level": "WARNING",
            "propagate": True,
        }
    },
}


# Sets default max upload size to 15MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 15728640

# Unique session cookie ensures that logins are treated separately for each app
SESSION_COOKIE_NAME = APP_NAME

# For more info on configuring your cache: https://docs.djangoproject.com/en/2.2/topics/cache/
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    },
    "user_permission": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "user_permission_cache",
    },
}

# Hide nodes and cards in a report that have no data
HIDE_EMPTY_NODES_IN_REPORT = False

BYPASS_UNIQUE_CONSTRAINT_TILE_VALIDATION = False
BYPASS_REQUIRED_VALUE_TILE_VALIDATION = False
PUBLIC_SERVER_ADDRESS = get_optional_env_variable(
    "PUBLIC_SERVER_ADDRESS", "http://localhost:8000/"
)
DATE_IMPORT_EXPORT_FORMAT = (
    "%Y-%m-%d"  # Custom date format for dates imported from and exported to csv
)


# This is used to indicate whether the data in the CSV and SHP exports should be
# ordered as seen in the resource cards or not.
EXPORT_DATA_FIELDS_IN_CARD_ORDER = False

# Identify the usernames and duration (seconds) for which you want to cache the time wheel
CACHE_BY_USER = {"anonymous": 3600 * 24}
TILE_CACHE_TIMEOUT = 600  # seconds
CLUSTER_DISTANCE_MAX = 5000  # meters
GRAPH_MODEL_CACHE_TIMEOUT = None

OAUTH_CLIENT_ID = ""  #'9JCibwrWQ4hwuGn5fu2u1oRZSs9V6gK8Vu8hpRC4'

APP_TITLE = "Arches | Heritage Data Management"
COPYRIGHT_TEXT = "All Rights Reserved."
COPYRIGHT_YEAR = "2019"

ENABLE_CAPTCHA = False
# RECAPTCHA_PUBLIC_KEY = ''
# RECAPTCHA_PRIVATE_KEY = ''
# RECAPTCHA_USE_SSL = False
NOCAPTCHA = True
# RECAPTCHA_PROXY = 'http://127.0.0.1:8000'
if DEBUG is True:
    SILENCED_SYSTEM_CHECKS = ["captcha.recaptcha_test_key_error"]


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  #<-- Only need to uncomment this for testing without an actual email server
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = "xxxx@xxx.com"
# EMAIL_HOST_PASSWORD = 'xxxxxxx'
# EMAIL_PORT = 587

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

CELERY_BROKER_URL = "amqp://{}:{}@localhost".format(
    get_optional_env_variable("RABBITMQ_USER", "guest"),
    get_optional_env_variable("RABBITMQ_PASS", "guest"),
)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_RESULT_BACKEND = (
    "django-db"  # Use 'django-cache' if you want to use your cache as your backend
)
CELERY_TASK_SERIALIZER = "json"


CELERY_SEARCH_EXPORT_EXPIRES = 24 * 3600  # seconds
CELERY_SEARCH_EXPORT_CHECK = 3600  # seconds

CELERY_BEAT_SCHEDULE = {
    "delete-expired-search-export": {
        "task": "arches.app.tasks.delete_file",
        "schedule": CELERY_SEARCH_EXPORT_CHECK,
    },
    "notification": {
        "task": "arches.app.tasks.message",
        "schedule": CELERY_SEARCH_EXPORT_CHECK,
        "args": ("Celery Beat is Running",),
    },
}

# Set to True if you want to send celery tasks to the broker without being able to detect celery.
# This might be necessary if the worker pool is regulary fully active, with no idle workers, or if
# you need to run the celery task using solo pool (e.g. on Windows). You may need to provide another
# way of monitoring celery so you can detect the background task not being available.
CELERY_CHECK_ONLY_INSPECT_BROKER = False

CANTALOUPE_DIR = os.path.join(ROOT_DIR, "uploadedfiles")
CANTALOUPE_HTTP_ENDPOINT = "http://localhost:8182/"

ACCESSIBILITY_MODE = False

# By setting RESTRICT_MEDIA_ACCESS to True, media file requests outside of Arches will checked against nodegroup permissions.
RESTRICT_MEDIA_ACCESS = False

# By setting RESTRICT_CELERY_EXPORT_FOR_ANONYMOUS_USER to True, if the user is attempting
# to export search results above the SEARCH_EXPORT_IMMEDIATE_DOWNLOAD_THRESHOLD
# value and is not signed in with a user account then the request will not be allowed.
RESTRICT_CELERY_EXPORT_FOR_ANONYMOUS_USER = False

# see https://docs.djangoproject.com/en/1.9/topics/i18n/translation/#how-django-discovers-language-preference
# to see how LocaleMiddleware tries to determine the user's language preference
# (make sure to check your accept headers as they will override the LANGUAGE_CODE setting!)
# also see get_language_from_request in django.utils.translation.trans_real.py
# to see how the language code is derived in the actual code

####### TO GENERATE .PO FILES DO THE FOLLOWING ########
# run the following commands
# language codes used in the command should be in the form (which is slightly different
# form the form used in the LANGUAGE_CODE and LANGUAGES settings below):
# --local={countrycode}_{REGIONCODE} <-- countrycode is lowercase, regioncode is uppercase, also notice the underscore instead of hyphen
# commands to run (to generate files for "British English, German, and Spanish"):
# django-admin.py makemessages --ignore=env/* --local=de --local=en --local=en_GB --local=es  --extension=htm,py
# django-admin.py compilemessages


# default language of the application
# language code needs to be all lower case with the form:
# {langcode}-{regioncode} eg: en, en-gb ....
# a list of language codes can be found here http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en"

# list of languages to display in the language switcher,
# if left empty or with a single entry then the switch won't be displayed
# language codes need to be all lower case with the form:
# {langcode}-{regioncode} eg: en, en-gb ....
# a list of language codes can be found here http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGES = [
    #   ('de', _('German')),
    ("en", _("English")),
    #   ('en-gb', _('British English')),
    #   ('es', _('Spanish')),
]

# override this to permenantly display/hide the language switcher
SHOW_LANGUAGE_SWITCH = len(LANGUAGES) > 1

try:
    from .package_settings import *
except ImportError:
    try:
        from package_settings import *
    except ImportError as e:
        pass

try:
    from .settings_local import *
except ImportError as e:
    try:
        from settings_local import *
    except ImportError as e:
        pass
# returns an output that can be read by NODEJS
if __name__ == "__main__":
    transmit_webpack_django_config(
        root_dir=ROOT_DIR,
        app_root=APP_ROOT,
        arches_applications=ARCHES_APPLICATIONS,
        public_server_address=PUBLIC_SERVER_ADDRESS,
        static_url=STATIC_URL,
        webpack_development_server_port=WEBPACK_DEVELOPMENT_SERVER_PORT,
    )
