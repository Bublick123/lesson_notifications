from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_lesson_notification(lesson_id, event_type, student_id):
    """
    Celery задача для отправки уведомления студенту.
    Имитирует отправку уведомления - просто логирует сообщение.
    
    ТОЧНО как в ТЗ: "Уведомление отправлено студенту [ID студента] 
    по уроку [Название урока]"
    """
    
    from django.apps import apps
    
    try:
        Lesson = apps.get_model('lesson_app', 'Lesson')
        lesson = Lesson.objects.get(id=lesson_id)
        
        
        message = (
            f"Уведомление отправлено студенту {student_id} "
            f"по уроку '{lesson.title}'"
        )
        
        
        logger.info(message)
        print(f"[Celery Task] {message}")
        
        
        return {
            'status': 'success',
            'lesson_id': lesson_id,
            'student_id': student_id,
            'lesson_title': lesson.title,
            'event_type': event_type,
            'message': message
        }
        
    except Exception as e:
        error_message = f"Ошибка при отправке уведомления: {str(e)}"
        logger.error(error_message)
        return {
            'status': 'error',
            'error': str(e)
        }