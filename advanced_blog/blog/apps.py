# blog/apps.py
from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    models_loaded = False  # Yeni flag ekleyin

    def ready(self):
        if not self.models_loaded:  # Sadece bir kez çalışmasını sağla
            import blog.signals
            self.models_loaded = True