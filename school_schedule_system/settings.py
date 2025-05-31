# Додайте 'school' до INSTALLED_APPS
INSTALLED_APPS = [
    ...,
    'school',
    ...
]

# Налаштування бази даних (можна використовувати SQLite за замовчуванням)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}