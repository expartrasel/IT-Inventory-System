from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q%a2(=m-glk=pmq3dn$^8(2i=5hec2-o_4-x0p6b++@&4tq$+v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'jazzmin',  # Must be at the top
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'assets',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inventory.urls'

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

WSGI_APPLICATION = 'inventory.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dhaka' 
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'

# ==============================================================================
# JAZZMIN SETTINGS (Admin UI Customization with Log Entries)
# ==============================================================================
JAZZMIN_SETTINGS = {
    "site_title": "NexMart Admin",
    "site_header": "NexMart IT",
    "site_brand": "NexMart Inventory",
    "welcome_sign": "Welcome to NexMart IT Inventory System",
    "copyright": "NexMart IT Solutions Ltd",
    "search_model": ["assets.Product", "assets.Supplier"],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "assets.Category": "fas fa-list",
        "assets.SubCategory": "fas fa-tags",
        "assets.Product": "fas fa-box",
        "assets.Supplier": "fas fa-truck",
        "assets.Outlet": "fas fa-store",
        "assets.Transfer": "fas fa-exchange-alt",
        "assets.TransferHistory": "fas fa-history",
        "admin.LogEntry": "fas fa-clipboard-list", # Activity Log Icon
    },
    "order_with_respect_to": [
        "assets.Category", 
        "assets.SubCategory", 
        "assets.Supplier", 
        "assets.Product", 
        "assets.Transfer", 
        "assets.TransferHistory", 
        "admin.LogEntry", # Placed for audit trail
        "assets.Outlet"
    ],
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly", 
    "navbar": "navbar-dark bg-dark",
    "sidebar": "sidebar-dark-primary",
}

# ==============================================================================
# EMAIL SETTINGS (For Low Stock Alerts)
# ==============================================================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com' 
EMAIL_HOST_PASSWORD = 'your-app-password' 
ADMIN_EMAIL = 'admin-email@gmail.com'