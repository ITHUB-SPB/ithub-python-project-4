from pathlib import Path
from core.settings.get_env import env


def get_database_settings() -> dict[str, str]:
    if env("PYTHON_ENVIRONMENT") != "PRODUCTION":
        return {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "students.sqlite3",
        }

    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.get("POSTGRES_DB"),
        "USER": env.get("POSTGRES_USER"),
        "PASSWORD": env.get("POSTGRES_PASSWORD"),
        "HOST": env.get("POSTGRES_HOST", "localhost"),
        "PORT": 5432,
    }


BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATABASES = {"default": get_database_settings()}
