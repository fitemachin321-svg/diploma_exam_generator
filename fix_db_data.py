import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from generator.models import QuestionTemplate

for q in QuestionTemplate.objects.filter(question_type='single'):
    if q.options_template and len(q.options_template) >= 2:
        # Оставляем ТОЛЬКО первые два варианта
        q.options_template = q.options_template[:2]
        q.save()
        print(f"Исправлен: {q.text_template[:50]}... (оставлено 2 варианта)")

print("\n✅ Готово! Теперь во всех тестовых вопросах ровно 2 варианта ответа.") 