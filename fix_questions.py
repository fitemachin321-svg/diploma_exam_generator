import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from generator.models import QuestionTemplate

# Убираем ? из вариантов ответов
for q in QuestionTemplate.objects.all():
    if q.options_template:
        changed = False
        new_options = []
        for opt in q.options_template:
            if opt.get('text') == '?':
                opt['text'] = 'Не знаю'
                changed = True
            new_options.append(opt)
        if changed:
            q.options_template = new_options
            q.save()
            print(f"Исправлен шаблон: {q.text_template[:50]}")

print("Готово!")