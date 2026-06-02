from pathlib import Path

from core.settings.get_env import env


BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    "unfold",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts.apps.AccountsConfig",
    "students.apps.StudentsConfig",
    "staff.apps.StaffConfig",
    "courses.apps.CoursesConfig",
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

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
            BASE_DIR / "students" / "templates",
            BASE_DIR / "accounts" / "templates",
            BASE_DIR / "courses" / "templates",
            BASE_DIR / "staff" / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DEBUG = env("PYTHON_ENVIRONMENT") == "DEVELOPMENT"
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "testserver"]

ROOT_URLCONF = "core.urls"
WSGI_APPLICATION = "core.wsgi.application"

LANGUAGE_CODE = "ru-RU"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "/auth/login"
LOGIN_REDIRECT_URL = "/courses"
LOGOUT_REDIRECT_URL = "/auth/login"
