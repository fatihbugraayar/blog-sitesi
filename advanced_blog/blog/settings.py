INSTALLED_APPS = [
    # ... existing code ...
    'ckeditor',
    'ckeditor_uploader',
]

# CKEditor ayarları
CKEDITOR_CONFIGS = {
    'default': {
        'width': '100%',
        'height': '300px',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source'],
            ['Image', 'Table'],
            ['Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
        ]
    }
}

# Medya dosyaları için CKEditor yükleme yolu
CKEDITOR_UPLOAD_PATH = "uploads/"
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ... existing code ... 