from django.contrib import admin
from .models import Lesson

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'is_completed', 'created_at')
    list_filter = ('is_completed', 'student')
    search_fields = ('title', 'student__username')

