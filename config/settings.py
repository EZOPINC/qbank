import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = os.environ.get
SECRET_KEY = env("SECRET_KEY", "dev-only-change-me")
DEBUG = env("DEBUG", "1") == "1"
ALLOWED_HOSTS = env("ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "bank",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [], "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages"]},
}]
DATABASES = {"default": {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": env("DB_NAME", "qbank"), "USER": env("DB_USER", "qbank"),
    "PASSWORD": env("DB_PASSWORD", "qbank"), "HOST": env("DB_HOST", "localhost"),
    "PORT": env("DB_PORT", "5432"),
}}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LANGUAGE_CODE = "en"; TIME_ZONE = "Asia/Kolkata"; USE_I18N = True; USE_TZ = True
STATIC_URL = "static/"
LOGIN_URL = "/accounts/login/"; LOGIN_REDIRECT_URL = "/"

# Source files live outside any web-served path; only login-protected views touch them.
PRIVATE_MEDIA_ROOT = Path(env("PRIVATE_MEDIA_ROOT", BASE_DIR / "private_media"))
MAX_UPLOAD_MB = int(env("MAX_UPLOAD_MB", "25"))
DATA_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_MB * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024

# Extraction
OCR_PROVIDER = env("OCR_PROVIDER", "bank.extraction.ocr.TesseractProvider")  # swap provider here
OCR_LANGS = env("OCR_LANGS", "eng+ben+hin")
PDF_COLUMNS = int(env("PDF_COLUMNS", "3"))   # printed columns per page (sample book is 3)
MIN_DIGITAL_CHARS = 50                         # fewer chars on a page -> treat as scanned -> OCR
LOW_CONFIDENCE = 0.80

# Celery (set CELERY_EAGER=0 with Redis running for real background processing)
CELERY_BROKER_URL = env("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_TASK_ALWAYS_EAGER = env("CELERY_EAGER", "1") == "1"

LOGGING = {
    "version": 1, "disable_existing_loggers": False,
    "formatters": {"kv": {"format": "ts=%(asctime)s level=%(levelname)s logger=%(name)s msg=%(message)s"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "kv"}},
    "loggers": {"bank": {"handlers": ["console"], "level": env("LOG_LEVEL", "INFO")}},
}
