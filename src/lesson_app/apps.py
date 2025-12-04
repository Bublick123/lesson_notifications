from django.apps import AppConfig

class LessonAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lesson_app'
    
    def ready(self):
        # Импортируем сигналы при запуске приложения
        import lesson_app.models  # сигналы уже в models.py