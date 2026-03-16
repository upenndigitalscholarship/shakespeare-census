import logging
import sys
from pathlib import Path

import environs
import structlog
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).parent.parent
APPS_DIR = BASE_DIR

env = environs.Env()

# We shouldn't load a .env file in any deployed context and rely on the
# container orchestration to inject values into the running environment
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    env.read_env(str(BASE_DIR / ".env"))
    print("The .env file has been loaded. See config/settings.py for more information")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=False)

# Local development flag
LOCAL_DEVELOPMENT = env.bool("LOCAL_DEVELOPMENT", default=False)

# Whether or not to use whitenoise
USE_WHITENOISE = env.bool("USE_WHITENOISE", default=DEBUG)

LOG_LEVEL = env.log_level("LOG_LEVEL", default="INFO")

#############################################################################
# Main Settings
#############################################################################
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

#############################################################################
# Security Settings
#############################################################################
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# Hosts
host_list = env.list(
    "DJANGO_ALLOWED_HOSTS", default=["localhost", "0.0.0.0", "127.0.0.1"]
)
ALLOWED_HOSTS = [el.strip() for el in host_list]
CSRF_TRUSTED_ORIGINS = [el.strip() for el in host_list]

# Site ID
SITE_ID = 1

#############################################################################
# Installed Apps
#############################################################################
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.admin",
]

THIRD_PARTY_APPS = [
    "django_extensions",
    "django_tailwind_cli",
]

# Local apps
LOCAL_APPS = [
    "users",
    "census",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

#############################################################################
# Middleware
#############################################################################
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

#############################################################################
# Templates
#############################################################################
DEFAULT_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

CACHED_LOADERS = [("django.template.loaders.cached.Loader", DEFAULT_LOADERS)]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR / "templates")],
        "OPTIONS": {
            "debug": DEBUG,
            "loaders": DEFAULT_LOADERS if DEBUG else CACHED_LOADERS,
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Crispy forms
CRISPY_TEMPLATE_PACK = "bootstrap4"

#############################################################################
# Authentication
#############################################################################
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_USER_MODEL = "users.User"

LOGIN_REDIRECT_URL = "users:redirect"
LOGIN_URL = "account_login"

#############################################################################
# Database
#############################################################################
try:
    DATABASES = {"default": env.dj_db_url("DATABASE_URL")}
except (ImproperlyConfigured, environs.EnvError):
    DATABASES = {
        "default": {
            "ENGINE": "django_db_geventpool.backends.postgresql_psycopg3",
            "HOST": env("PGHOST"),
            "NAME": env("PGDATABASE"),
            "PASSWORD": env("PGPASSWORD", default=""),
            "PORT": env.int("PGPORT", default=5432),
            "USER": env("PGUSER"),
            "CONN_MAX_AGE": 0,
            "OPTIONS": {"MAX_CONNS": 10},
        }
    }

# Default auto field
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

#############################################################################
# Cache
#############################################################################
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

#############################################################################
# Internationalization
#############################################################################
LANGUAGE_CODE = "en-us"
USE_I18N = True
TIME_ZONE = "UTC"
USE_TZ = True

#############################################################################
# Static files
#############################################################################
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR.joinpath("deployed_static").as_posix()
STATICFILES_DIRS = [BASE_DIR.joinpath("static").as_posix()]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# WhiteNoise for static files
if USE_WHITENOISE:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_AUTOREFRESH = True

#############################################################################
# Media files
#############################################################################
MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR / "media")

#############################################################################
# Email
#############################################################################
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="Shakespeare Census <noreply@shakespearecensus.org>",
)
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
EMAIL_SUBJECT_PREFIX = env(
    "DJANGO_EMAIL_SUBJECT_PREFIX", default="[Shakespeare Census]"
)

EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025


#############################################################################
# Logging setup
#############################################################################
root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stderr)
root.addHandler(handler)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
        "plain_console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
        },
        "key_value": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.KeyValueRenderer(
                key_order=["event", "logger"]
            ),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "plain_console",
        },
        "json": {
            "class": "logging.StreamHandler",
            "formatter": "json_formatter",
        },
        "kv": {
            "class": "logging.StreamHandler",
            "formatter": "key_value",
        },
    },
    "loggers": {
        "": {
            "handlers": ["json"],
            "level": LOG_LEVEL,  # defaults to INFO
        },
    },
}

# Configure struct log
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

#############################################################################
# Tailwind CLI Settings
#############################################################################
TAILWIND_CLI_AUTOMATIC_DOWNLOAD = True
TAILWIND_CLI_DIST_CSS = "css/tailwind.min.css"
TAILWIND_CLI_SRC_CSS = "static/css/input.css"
