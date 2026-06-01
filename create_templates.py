import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from generator.models import Subject, Topic, QuestionTemplate

# Создаём предмет
subject, _ = Subject.objects.get_or_create(
    name="Математика",
    defaults={"description": "Основные математические темы", "created_by_id": 1}
)
print(f"Предмет: {subject.name}\n")

def create_topic(name, content, difficulty):
    topic, _ = Topic.objects.get_or_create(
        subject=subject,
        title=name,
        defaults={"content": content, "difficulty_level": difficulty}
    )
    print(f"Тема: {topic.title}")
    return topic

def add_open_question(topic, text, answer_template, points=2):
    """Добавляет открытый вопрос с шаблоном ответа"""
    obj, created = QuestionTemplate.objects.get_or_create(
        topic=topic,
        text_template=text,
        defaults={
            "question_type": "open",
            "correct_answer_template": answer_template,
            "points": points
        }
    )
    if not created:
        obj.correct_answer_template = answer_template
        obj.save()
    return obj

def add_single_question(topic, text, correct, wrong1, wrong2, points=2):
    """Добавляет тестовый вопрос с вариантами ответов"""
    options = [
        {"text": str(correct), "is_correct": True},
        {"text": str(wrong1), "is_correct": False},
        {"text": str(wrong2), "is_correct": False}
    ]
    obj, created = QuestionTemplate.objects.get_or_create(
        topic=topic,
        text_template=text,
        defaults={
            "question_type": "single",
            "correct_answer_template": str(correct),
            "options_template": options,
            "points": points
        }
    )
    if not created:
        obj.correct_answer_template = str(correct)
        obj.options_template = options
        obj.save()
    return obj

# ===== 1. Сложение чисел (8 открытых + 7 тестовых) =====
topic1 = create_topic("Сложение чисел", "Сложение двух чисел", 1)
open1 = [
    ("{a} + {b} =", "{a+b}"),
    ("{a} + {b} + {c} =", "{a+b+c}"),
    ("{a} + 0 =", "{a}"),
    ("0 + {a} =", "{a}"),
    ("{a} + (-{b}) =", "{a-b}"),
    ("(-{a}) + {b} =", "{-a+b}"),
    ("{a} + {b} + {c} + {d} =", "{a+b+c+d}"),
    ("{a} + ({b} + {c}) =", "{a+b+c}"),
]
for text, ans in open1:
    add_open_question(topic1, text, ans)
print(f"  Добавлено {len(open1)} открытых")

single1 = [
    ("5 + 3 =", 8, 7, 9),
    ("10 + 2 =", 12, 11, 13),
    ("7 + 6 =", 13, 12, 14),
    ("4 + 9 =", 13, 12, 14),
    ("8 + 8 =", 16, 15, 17),
    ("20 + 30 =", 50, 40, 60),
    ("15 + 5 =", 20, 18, 22),
]
for text, cor, w1, w2 in single1:
    add_single_question(topic1, text, cor, w1, w2)
print(f"  Добавлено {len(single1)} тестовых")

# ===== 2. Вычитание чисел (8 открытых + 7 тестовых) =====
topic2 = create_topic("Вычитание чисел", "Вычитание двух чисел", 1)
open2 = [
    ("{a} - {b} =", "{a-b}"),
    ("{a} - {b} - {c} =", "{a-b-c}"),
    ("{a} - 0 =", "{a}"),
    ("0 - {a} =", "{-a}"),
    ("{a} - (-{b}) =", "{a+b}"),
    ("(-{a}) - {b} =", "{-a-b}"),
    ("{a} - {b} + {c} =", "{a-b+c}"),
    ("{a} + {b} - {c} =", "{a+b-c}"),
]
for text, ans in open2:
    add_open_question(topic2, text, ans)
print(f"  Добавлено {len(open2)} открытых")

single2 = [
    ("10 - 3 =", 7, 6, 8),
    ("20 - 5 =", 15, 14, 16),
    ("15 - 7 =", 8, 7, 9),
    ("100 - 30 =", 70, 60, 80),
    ("50 - 25 =", 25, 20, 30),
    ("9 - 4 =", 5, 4, 6),
    ("30 - 10 =", 20, 10, 40),
]
for text, cor, w1, w2 in single2:
    add_single_question(topic2, text, cor, w1, w2)
print(f"  Добавлено {len(single2)} тестовых")

# ===== 3. Умножение чисел (8 открытых + 7 тестовых) =====
topic3 = create_topic("Умножение чисел", "Умножение двух чисел", 2)
open3 = [
    ("{a} × {b} =", "{a*b}"),
    ("{a} × {b} × {c} =", "{a*b*c}"),
    ("{a} × 0 =", "0"),
    ("{a} × 1 =", "{a}"),
    ("(-{a}) × {b} =", "{-a*b}"),
    ("{a} × (-{b}) =", "{-a*b}"),
    ("{a} × {b} + {c} =", "{a*b+c}"),
    ("{a} × {b} - {c} =", "{a*b-c}"),
]
for text, ans in open3:
    add_open_question(topic3, text, ans)
print(f"  Добавлено {len(open3)} открытых")

single3 = [
    ("5 × 6 =", 30, 35, 25),
    ("8 × 7 =", 56, 48, 64),
    ("4 × 25 =", 100, 90, 110),
    ("3 × 8 =", 24, 21, 27),
    ("6 × 9 =", 54, 56, 52),
    ("7 × 8 =", 56, 54, 58),
    ("9 × 9 =", 81, 72, 90),
]
for text, cor, w1, w2 in single3:
    add_single_question(topic3, text, cor, w1, w2)
print(f"  Добавлено {len(single3)} тестовых")

# ===== 4. Деление чисел (8 открытых + 7 тестовых) =====
topic4 = create_topic("Деление чисел", "Деление двух чисел", 2)
open4 = [
    ("{a} ÷ {b} =", "{a/b}"),
    ("{a} ÷ 1 =", "{a}"),
    ("0 ÷ {a} =", "0"),
    ("(-{a}) ÷ {b} =", "{-a/b}"),
    ("{a} ÷ (-{b}) =", "{-a/b}"),
    ("{a} ÷ {b} + {c} =", "{a/b+c}"),
    ("{a} ÷ {b} - {c} =", "{a/b-c}"),
    ("({a} + {b}) ÷ {c} =", "{(a+b)/c}"),
]
for text, ans in open4:
    add_open_question(topic4, text, ans)
print(f"  Добавлено {len(open4)} открытых")

single4 = [
    ("10 ÷ 2 =", 5, 4, 6),
    ("20 ÷ 4 =", 5, 4, 6),
    ("100 ÷ 10 =", 10, 20, 5),
    ("15 ÷ 3 =", 5, 6, 4),
    ("25 ÷ 5 =", 5, 4, 6),
    ("12 ÷ 4 =", 3, 4, 2),
    ("30 ÷ 5 =", 6, 5, 7),
]
for text, cor, w1, w2 in single4:
    add_single_question(topic4, text, cor, w1, w2)
print(f"  Добавлено {len(single4)} тестовых")

# ===== 5. Чётные и нечётные числа (5 открытых + 10 тестовых) =====
topic5 = create_topic("Чётные и нечётные числа", "Определение чётности", 1)
open5 = [
    ("Чётное число делится на", "2"),
    ("Последняя цифра чётного числа", "0,2,4,6,8"),
    ("Последняя цифра нечётного числа", "1,3,5,7,9"),
    ("Сумма двух чётных чисел", "чётная"),
    ("Сумма двух нечётных чисел", "чётная"),
]
for text, ans in open5:
    add_open_question(topic5, text, ans)
print(f"  Добавлено {len(open5)} открытых")

single5 = [
    ("2 — это", "чётное число", "нечётное число", "?"),
    ("3 — это", "нечётное число", "чётное число", "?"),
    ("4 — это", "чётное число", "нечётное число", "?"),
    ("5 — это", "нечётное число", "чётное число", "?"),
    ("0 — это", "чётное число", "нечётное число", "?"),
    ("6 — это", "чётное число", "нечётное число", "?"),
    ("7 — это", "нечётное число", "чётное число", "?"),
    ("8 — это", "чётное число", "нечётное число", "?"),
    ("9 — это", "нечётное число", "чётное число", "?"),
    ("10 — это", "чётное число", "нечётное число", "?"),
]
for text, cor, w1, w2 in single5:
    add_single_question(topic5, text, cor, w1, w2)
print(f"  Добавлено {len(single5)} тестовых")

# ===== 6. Простые и составные числа (5 открытых + 10 тестовых) =====
topic6 = create_topic("Простые и составные числа", "Определение простых чисел", 2)
open6 = [
    ("Наименьшее простое число", "2"),
    ("Простые числа имеют", "два делителя"),
    ("Составные числа имеют", "больше двух делителей"),
    ("Число 1", "ни простое, ни составное"),
    ("Простых чисел", "бесконечно много"),
]
for text, ans in open6:
    add_open_question(topic6, text, ans)
print(f"  Добавлено {len(open6)} открытых")

single6 = [
    ("2 — это", "простое", "составное", "?"),
    ("3 — это", "простое", "составное", "?"),
    ("4 — это", "составное", "простое", "?"),
    ("5 — это", "простое", "составное", "?"),
    ("6 — это", "составное", "простое", "?"),
    ("7 — это", "простое", "составное", "?"),
    ("8 — это", "составное", "простое", "?"),
    ("9 — это", "составное", "простое", "?"),
    ("10 — это", "составное", "простое", "?"),
    ("11 — это", "простое", "составное", "?"),
]
for text, cor, w1, w2 in single6:
    add_single_question(topic6, text, cor, w1, w2)
print(f"  Добавлено {len(single6)} тестовых")

print("\n" + "="*60)
print("✅ ГОТОВО!")
print("📚 6 тем")
print("📝 90 шаблонов (47 открытых + 43 тестовых)")
print("="*60)