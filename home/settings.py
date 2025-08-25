from pathlib import Path
import environ
from datetime import timedelta
import dj_database_url
import os

# --- Base directory ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Django-environ init ---
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(BASE_DIR / ".env")

# --- Core settings ---
SECRET_KEY = env("SECRET_KEY", default="django-insecure-abc123xyz")
DEBUG = env("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

# --- Installed apps ---
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project apps
    'reklamaproject',

    # DRF
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',

    # Auth
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Swagger
    'drf_spectacular',

    # Security
    'axes',
    'corsheaders',
]

# --- Middleware ---
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]

# --- CORS / CSRF ---
# CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=False)
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://marketing-five-rose.vercel.app",
    "https://2abfcea964d1.ngrok-free.app",
])
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://marketing-five-rose.vercel.app",
    "https://2abfcea964d1.ngrok-free.app",
])

# --- URL ---
ROOT_URLCONF = 'home.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'home.wsgi.application'

# DATABASES = {
#     'default': dj_database_url.config(
#         default=os.environ.get("DATABASE_URL")
#     )
# }


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "reklamaproject",
        "USER": "postgres",
        "PASSWORD": "sunnat1123",
        "HOST": "localhost",
        "PORT": "5433",
    }
}



# --- Auth ---
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'axes.backends.AxesStandaloneBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 7, 
} 

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# --- Internationalization ---
LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# --- Static & Media ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- Site ---
SITE_ID = 1
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Jazzmin ---
JAZZMIN_SETTINGS = {
    "site_title": "Reklama Paneli",
    "site_header": "Metro Reklama Admin",
    "site_brand": "Metro Reklama",
    "welcome_sign": "Xush kelibsiz, admin!",
    "copyright": "© 2025 Metro",
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "reklamaproject.Station": "fas fa-subway",
        "reklamaproject.Advertisement": "fas fa-bullhorn",
        "reklamaproject.Position": "fas fa-map-marker-alt",
        "reklamaproject.MetroLine": "fas fa-subway",
        "reklamaproject.AdvertisementArchive": "fas fa-archive",
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users-cog",
        "authtoken.Token": "fas fa-key",
        "axes.AccessAttempt": "fas fa-sign-in-alt",
        "axes.AccessFailureLog": "fas fa-times-circle",
        "axes.AccessLog": "fas fa-history",
        "account.EmailAddress": "fas fa-envelope",
        "socialaccount.SocialAccount": "fas fa-globe",
        "socialaccount.SocialApp": "fab fa-app-store",
        "socialaccount.SocialToken": "fas fa-id-badge",
    },
}

JAZZMIN_UI_TWEAKS = {
    "brand_colour": "navbar-success",
    "accent": "accent-teal",
    "navbar": "navbar-dark",
    "sidebar": "sidebar-dark-info",
    "theme": "cyborg",
}

# --- Swagger ---
SPECTACULAR_SETTINGS = {
    'TITLE': 'DRF tarmoq',
    'DESCRIPTION': 'Drf reklama',
    'VERSION': '1.0.0',
}
