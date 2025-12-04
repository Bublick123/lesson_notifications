from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import send_lesson_notification

class Lesson(models.Model):
    """Модель Урока - ТОЛЬКО необходимые поля по ТЗ"""
    title = models.CharField(max_length=200)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.student.username}"
    
    def complete(self):
        """Метод для завершения урока"""
        self.is_completed = True
        self.save()

# Сигнал для отслеживания создания урока
@receiver(post_save, sender=Lesson)
def lesson_created_handler(sender, instance, created, **kwargs):
    """
    Отслеживаем важное событие - создание урока.
    Запускаем Celery задачу асинхронно.
    """
    if created:
        # Событие создания урока
        send_lesson_notification.delay(
            lesson_id=instance.id,
            event_type='created',
            student_id=instance.student_id
        )
    
    # Отслеживаем завершение урока
    if not created and instance.is_completed:
        # Событие завершения урока
        send_lesson_notification.delay(
            lesson_id=instance.id,
            event_type='completed',
            student_id=instance.student_id
        )