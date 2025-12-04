#!/bin/bash
echo "1. Creating migrations..."
docker-compose exec web python manage.py makemigrations lesson_app

echo "2. Applying migrations..."
docker-compose exec web python manage.py migrate

echo "3. Creating admin.py..."
cat > src/lesson_app/admin.py << 'EOF'
from django.contrib import admin
from .models import Lesson

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'is_completed', 'created_at')
    list_filter = ('is_completed', 'student')
    search_fields = ('title', 'student__username')
EOF

echo "4. Restarting web server..."
docker-compose restart web

echo "5. Done! Check http://localhost:8000/admin"