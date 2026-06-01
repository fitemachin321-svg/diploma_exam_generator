import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from generator.models import Subject, Topic, QuestionTemplate

# Удаляем всё существующее
print("Удаляем старые данные...")
Subject.objects.all().delete()  # удалит всё каскадно
print("Все старые предметы, темы и шаблоны удалены.\n")

# Создаём предмет
subject = Subject.objects.create(
    name="Математика",
    description="Основные математические темы",
    created_by_id=1  # предполагаем, что есть суперпользователь с id=1
)
print(f"Создан предмет: {subject.name}\n")

def create_topic(name, content, difficulty):
    topic = Topic.objects.create(
        subject=subject,
        title=name,
        content=content,
        difficulty_level=difficulty
    )
    print(f"  Тема: {topic.title}")
    return topic

def add_open_question(topic, text, answer):
    """Добавляет открытый вопрос"""
    q = QuestionTemplate.objects.create(
        topic=topic,
        question_type='open',
        text_template=text,
        correct_answer_template=answer,
        points=2
    )
    return q

def add_single_question(topic, text, correct, wrong):
    """Добавляет тестовый вопрос с двумя вариантами (правильный и один неправильный)"""
    options = [
        {"text": str(correct), "is_correct": True},
        {"text": str(wrong), "is_correct": False}
    ]
    q = QuestionTemplate.objects.create(
        topic=topic,
        question_type='single',
        text_template=text,
        correct_answer_template=str(correct),
        options_template=options,
        points=2
    )
    return q

# ===== 1. Сложение чисел =====
topic1 = create_topic("Сложение чисел", "Сложение двух и трёх чисел", 1)

# Открытые вопросы (7 штук)
open1 = [
    ("0 + 0 =", "0"),
    ("0 + 5 =", "5"),
    ("5 + 0 =", "5"),
    ("{a} + {b} =", "{a+b}"),
    ("{a} + {b} + {c} =", "{a+b+c}"),
    ("{a} + 0 =", "{a}"),
    ("0 + {a} =", "{a}"),
]
for text, ans in open1:
    add_open_question(topic1, text, ans)

# Тестовые вопросы (8 штук)
single1 = [
    ("5 + 3 =", 8, 7),
    ("10 + 2 =", 12, 11),
    ("7 + 6 =", 13, 14),
    ("4 + 9 =", 13, 12),
    ("8 + 8 =", 16, 15),
    ("20 + 30 =", 50, 40),
    ("15 + 5 =", 20, 18),
    ("12 + 8 =", 20, 19),
]
for text, correct, wrong in single1:
    add_single_question(topic1, text, correct, wrong)
print(f"    Добавлено {len(open1)} открытых + {len(single1)} тестовых = 15\n")

# ===== 2. Вычитание чисел =====
topic2 = create_topic("Вычитание чисел", "Вычитание двух чисел", 1)

open2 = [
    ("0 - 0 =", "0"),
    ("0 - 5 =", "-5"),
    ("5 - 0 =", "5"),
    ("{a} - {b} =", "{a-b}"),
    ("{a} - {b} - {c} =", "{a-b-c}"),
    ("{a} - 0 =", "{a}"),
    ("0 - {a} =", "{-a}"),
]
for text, ans in open2:
    add_open_question(topic2, text, ans)

single2 = [
    ("10 - 3 =", 7, 8),
    ("20 - 5 =", 15, 14),
    ("15 - 7 =", 8, 9),
    ("100 - 30 =", 70, 80),
    ("50 - 25 =", 25, 30),
    ("9 - 4 =", 5, 6),
    ("30 - 10 =", 20, 40),
    ("18 - 9 =", 9, 10),
]
for text, correct, wrong in single2:
    add_single_question(topic2, text, correct, wrong)
print(f"    Добавлено {len(open2)} открытых + {len(single2)} тестовых = 15\n")

# ===== 3. Умножение чисел =====
topic3 = create_topic("Умножение чисел", "Умножение двух чисел", 2)

open3 = [
    ("0 × 5 =", "0"),
    ("5 × 0 =", "0"),
    ("1 × {a} =", "{a}"),
    ("{a} × 1 =", "{a}"),
    ("{a} × {b} =", "{a*b}"),
    ("{a} × {b} × {c} =", "{a*b*c}"),
    ("(-{a}) × {b} =", "{-a*b}"),
]
for text, ans in open3:
    add_open_question(topic3, text, ans)

single3 = [
    ("5 × 6 =", 30, 35),
    ("8 × 7 =", 56, 48),
    ("4 × 25 =", 100, 90),
    ("3 × 8 =", 24, 27),
    ("6 × 9 =", 54, 52),
    ("7 × 8 =", 56, 54),
    ("9 × 9 =", 81, 72),
    ("12 × 12 =", 144, 132),
]
for text, correct, wrong in single3:
    add_single_question(topic3, text, correct, wrong)
print(f"    Добавлено {len(open3)} открытых + {len(single3)} тестовых = 15\n")

# ===== 4. Деление чисел =====
topic4 = create_topic("Деление чисел", "Деление двух чисел", 2)

open4 = [
    ("0 ÷ 5 =", "0"),
    ("{a} ÷ 1 =", "{a}"),
    ("{a} ÷ {b} =", "{a/b}"),
    ("(-{a}) ÷ {b} =", "{-a/b}"),
    ("{a} ÷ (-{b}) =", "{-a/b}"),
    ("{a} ÷ {b} + {c} =", "{a/b + c}"),
    ("({a} + {b}) ÷ {c} =", "{(a+b)/c}"),
]
for text, ans in open4:
    add_open_question(topic4, text, ans)

single4 = [
    ("10 ÷ 2 =", 5, 4),
    ("20 ÷ 4 =", 5, 6),
    ("100 ÷ 10 =", 10, 20),
    ("15 ÷ 3 =", 5, 6),
    ("25 ÷ 5 =", 5, 4),
    ("12 ÷ 4 =", 3, 4),
    ("30 ÷ 5 =", 6, 5),
    ("18 ÷ 3 =", 6, 5),
]
for text, correct, wrong in single4:
    add_single_question(topic4, text, correct, wrong)
print(f"    Добавлено {len(open4)} открытых + {len(single4)} тестовых = 15\n")

# ===== 5. Чётные и нечётные числа =====
topic5 = create_topic("Чётные и нечётные числа", "Определение чётности", 1)

open5 = [
    ("Чётное число делится на", "2"),
    ("Последняя цифра чётного числа", "0,2,4,6,8"),
    ("Последняя цифра нечётного числа", "1,3,5,7,9"),
    ("Сумма двух чётных чисел", "чётная"),
    ("Сумма двух нечётных чисел", "чётная"),
    ("Сумма чётного и нечётного числа", "нечётная"),
]
for text, ans in open5:
    add_open_question(topic5, text, ans)

single5 = [
    ("2 — это", "чётное число", "нечётное число"),
    ("3 — это", "нечётное число", "чётное число"),
    ("4 — это", "чётное число", "нечётное число"),
    ("5 — это", "нечётное число", "чётное число"),
    ("0 — это", "чётное число", "нечётное число"),
    ("6 — это", "чётное число", "нечётное число"),
    ("7 — это", "нечётное число", "чётное число"),
    ("8 — это", "чётное число", "нечётное число"),
    ("9 — это", "нечётное число", "чётное число"),
]
for text, correct, wrong in single5:
    add_single_question(topic5, text, correct, wrong)
print(f"    Добавлено {len(open5)} открытых + {len(single5)} тестовых = 15\n")

# ===== 6. Простые и составные числа =====
topic6 = create_topic("Простые и составные числа", "Определение простых чисел", 2)

open6 = [
    ("Наименьшее простое число", "2"),
    ("Простые числа имеют", "два делителя"),
    ("Число 1", "ни простое, ни составное"),
    ("Простых чисел", "бесконечно много"),
    ("Составные числа имеют", "больше двух делителей"),
]
for text, ans in open6:
    add_open_question(topic6, text, ans)

single6 = [
    ("2 — это", "простое", "составное"),
    ("3 — это", "простое", "составное"),
    ("4 — это", "составное", "простое"),
    ("5 — это", "простое", "составное"),
    ("6 — это", "составное", "простое"),
    ("7 — это", "простое", "составное"),
    ("8 — это", "составное", "простое"),
    ("9 — это", "составное", "простое"),
    ("10 — это", "составное", "простое"),
    ("11 — это", "простое", "составное"),
]
for text, correct, wrong in single6:
    add_single_question(topic6, text, correct, wrong)
print(f"    Добавлено {len(open6)} открытых + {len(single6)} тестовых = 15\n")

print("="*60)
print("✅ ГОТОВО! Создано 6 тем, 90 шаблонов (открытые + тестовые с 2 вариантами).")
print("="*60)