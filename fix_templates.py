import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from generator.models import Subject, Topic, QuestionTemplate

# Удаляем старые проблемные темы
Topic.objects.filter(title__in=[
    "Модуль числа", 
    "Округление чисел", 
    "Степень числа 2", 
    "Сравнение чисел"
]).delete()

subject = Subject.objects.first()

# ===== ТОЛЬКО РАБОЧИЕ ТЕМЫ =====
data = [
    {
        "topic": "Сложение чисел",
        "difficulty": 1,
        "templates": [
            {"text": "5 + 7 =", "answer": "12", "options": "12|13|11"},
            {"text": "10 + 20 =", "answer": "30", "options": "30|40|20"},
            {"text": "8 + 9 =", "answer": "17", "options": "17|18|16"},
            {"text": "15 + 25 =", "answer": "40", "options": "40|50|35"},
            {"text": "6 + 6 =", "answer": "12", "options": "12|11|13"},
            {"text": "100 + 200 =", "answer": "300", "options": "300|400|200"},
            {"text": "3 + 4 =", "answer": "7", "options": "7|8|6"},
            {"text": "25 + 25 =", "answer": "50", "options": "50|45|55"},
            {"text": "12 + 8 =", "answer": "20", "options": "20|18|22"},
            {"text": "14 + 6 =", "answer": "20", "options": "20|19|21"},
            {"text": "9 + 9 =", "answer": "18", "options": "18|17|19"},
            {"text": "30 + 20 =", "answer": "50", "options": "50|40|60"},
            {"text": "7 + 8 =", "answer": "15", "options": "15|14|16"},
            {"text": "4 + 9 =", "answer": "13", "options": "13|12|14"},
            {"text": "1 + 9 =", "answer": "10", "options": "10|9|11"},
        ]
    },
    {
        "topic": "Вычитание чисел",
        "difficulty": 1,
        "templates": [
            {"text": "10 - 3 =", "answer": "7", "options": "7|8|6"},
            {"text": "20 - 15 =", "answer": "5", "options": "5|10|15"},
            {"text": "100 - 30 =", "answer": "70", "options": "70|80|60"},
            {"text": "50 - 25 =", "answer": "25", "options": "25|20|30"},
            {"text": "9 - 4 =", "answer": "5", "options": "5|6|4"},
            {"text": "15 - 7 =", "answer": "8", "options": "8|7|9"},
            {"text": "30 - 10 =", "answer": "20", "options": "20|10|40"},
            {"text": "18 - 9 =", "answer": "9", "options": "9|10|8"},
            {"text": "100 - 50 =", "answer": "50", "options": "50|40|60"},
            {"text": "25 - 10 =", "answer": "15", "options": "15|14|16"},
            {"text": "40 - 30 =", "answer": "10", "options": "10|20|5"},
            {"text": "12 - 5 =", "answer": "7", "options": "7|6|8"},
            {"text": "21 - 7 =", "answer": "14", "options": "14|13|15"},
            {"text": "8 - 3 =", "answer": "5", "options": "5|4|6"},
            {"text": "16 - 9 =", "answer": "7", "options": "7|8|6"},
        ]
    },
    {
        "topic": "Умножение чисел",
        "difficulty": 2,
        "templates": [
            {"text": "5 × 6 =", "answer": "30", "options": "30|35|25"},
            {"text": "8 × 7 =", "answer": "56", "options": "56|48|64"},
            {"text": "4 × 25 =", "answer": "100", "options": "100|90|110"},
            {"text": "3 × 8 =", "answer": "24", "options": "24|21|27"},
            {"text": "6 × 9 =", "answer": "54", "options": "54|56|52"},
            {"text": "7 × 8 =", "answer": "56", "options": "56|54|58"},
            {"text": "9 × 9 =", "answer": "81", "options": "81|72|90"},
            {"text": "12 × 12 =", "answer": "144", "options": "144|132|156"},
            {"text": "2 × 25 =", "answer": "50", "options": "50|45|55"},
            {"text": "10 × 10 =", "answer": "100", "options": "100|90|110"},
            {"text": "4 × 6 =", "answer": "24", "options": "24|22|26"},
            {"text": "7 × 7 =", "answer": "49", "options": "49|48|50"},
            {"text": "3 × 9 =", "answer": "27", "options": "27|26|28"},
            {"text": "5 × 5 =", "answer": "25", "options": "25|20|30"},
            {"text": "8 × 8 =", "answer": "64", "options": "64|56|72"},
        ]
    },
    {
        "topic": "Деление чисел",
        "difficulty": 2,
        "templates": [
            {"text": "10 ÷ 2 =", "answer": "5", "options": "5|4|6"},
            {"text": "20 ÷ 4 =", "answer": "5", "options": "5|4|6"},
            {"text": "100 ÷ 10 =", "answer": "10", "options": "10|20|5"},
            {"text": "15 ÷ 3 =", "answer": "5", "options": "5|6|4"},
            {"text": "25 ÷ 5 =", "answer": "5", "options": "5|4|6"},
            {"text": "12 ÷ 4 =", "answer": "3", "options": "3|4|2"},
            {"text": "30 ÷ 5 =", "answer": "6", "options": "6|5|7"},
            {"text": "18 ÷ 3 =", "answer": "6", "options": "6|5|7"},
            {"text": "42 ÷ 6 =", "answer": "7", "options": "7|6|8"},
            {"text": "81 ÷ 9 =", "answer": "9", "options": "9|8|10"},
            {"text": "14 ÷ 2 =", "answer": "7", "options": "7|6|8"},
            {"text": "24 ÷ 3 =", "answer": "8", "options": "8|7|9"},
            {"text": "32 ÷ 8 =", "answer": "4", "options": "4|5|3"},
            {"text": "45 ÷ 5 =", "answer": "9", "options": "9|8|10"},
            {"text": "36 ÷ 6 =", "answer": "6", "options": "6|5|7"},
        ]
    },
    {
        "topic": "Чётные и нечётные числа",
        "difficulty": 1,
        "templates": [
            {"text": "Число 2 является", "answer": "чётным", "options": "чётным|нечётным|?"},
            {"text": "Число 3 является", "answer": "нечётным", "options": "нечётным|чётным|?"},
            {"text": "Число 4 является", "answer": "чётным", "options": "чётным|нечётным|?"},
            {"text": "Число 5 является", "answer": "нечётным", "options": "нечётным|чётным|?"},
            {"text": "Число 0 является", "answer": "чётным", "options": "чётным|нечётным|?"},
            {"text": "Чётное число делится на", "answer": "2", "options": "2|3|4"},
            {"text": "Сумма двух чётных чисел", "answer": "чётная", "options": "чётная|нечётная|?"},
            {"text": "Сумма двух нечётных чисел", "answer": "чётная", "options": "чётная|нечётная|?"},
            {"text": "Сумма чётного и нечётного числа", "answer": "нечётная", "options": "нечётная|чётная|?"},
            {"text": "Последняя цифра чётного числа", "answer": "0,2,4,6,8", "options": "0,2,4,6,8|1,3,5,7,9|0,5"},
            {"text": "Последняя цифра нечётного числа", "answer": "1,3,5,7,9", "options": "1,3,5,7,9|0,2,4,6,8|0,5"},
            {"text": "Число 6 является", "answer": "чётным", "options": "чётным|нечётным|?"},
            {"text": "Число 7 является", "answer": "нечётным", "options": "нечётным|чётным|?"},
            {"text": "Число 10 является", "answer": "чётным", "options": "чётным|нечётным|?"},
            {"text": "Число 11 является", "answer": "нечётным", "options": "нечётным|чётным|?"},
        ]
    },
    {
        "topic": "Простые и составные числа",
        "difficulty": 2,
        "templates": [
            {"text": "Наименьшее простое число", "answer": "2", "options": "2|3|1"},
            {"text": "Число 2 является", "answer": "простым", "options": "простым|составным|?"},
            {"text": "Число 3 является", "answer": "простым", "options": "простым|составным|?"},
            {"text": "Число 4 является", "answer": "составным", "options": "составным|простым|?"},
            {"text": "Число 5 является", "answer": "простым", "options": "простым|составным|?"},
            {"text": "Число 6 является", "answer": "составным", "options": "составным|простым|?"},
            {"text": "Число 7 является", "answer": "простым", "options": "простым|составным|?"},
            {"text": "Число 8 является", "answer": "составным", "options": "составным|простым|?"},
            {"text": "Число 9 является", "answer": "составным", "options": "составным|простым|?"},
            {"text": "Число 10 является", "answer": "составным", "options": "составным|простым|?"},
            {"text": "Число 11 является", "answer": "простым", "options": "простым|составным|?"},
            {"text": "Число 12 является", "answer": "составным", "options": "составным|простым|?"},
            {"text": "Число 13 является", "answer": "простым", "options": "простым|составным|?"},
            {"text": "Число 14 является", "answer": "составным", "options": "составным|простым|?"},
            {"text": "Число 17 является", "answer": "простым", "options": "простым|составным|?"},
        ]
    },
]

def parse_options(options_str):
    opts = options_str.split('|')
    while len(opts) < 3:
        opts.append("?")
    return [
        {"text": opts[0], "is_correct": True},
        {"text": opts[1], "is_correct": False},
        {"text": opts[2], "is_correct": False}
    ]

for topic_data in data:
    topic, _ = Topic.objects.get_or_create(
        subject=subject,
        title=topic_data["topic"],
        defaults={"content": topic_data["topic"], "difficulty_level": topic_data["difficulty"]}
    )
    print(f"Тема: {topic.title}")
    
    for tmpl in topic_data["templates"]:
        options_json = parse_options(tmpl["options"])
        
        existing = QuestionTemplate.objects.filter(topic=topic, text_template=tmpl["text"]).first()
        if existing:
            existing.correct_answer_template = tmpl["answer"]
            existing.options_template = options_json
            existing.points = 2
            existing.save()
            print(f"  Обновлён: {tmpl['text']}")
        else:
            QuestionTemplate.objects.create(
                topic=topic,
                question_type="single",
                text_template=tmpl["text"],
                correct_answer_template=tmpl["answer"],
                options_template=options_json,
                points=2
            )
            print(f"  Создан: {tmpl['text']}")

print("\n✅ Готово! Осталось 6 рабочих тем.")