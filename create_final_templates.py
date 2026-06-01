import os
import django
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from generator.models import Subject, Topic, QuestionTemplate

# Удаляем всё
print("Удаляем старые данные...")
Subject.objects.all().delete()
print("Удалено.\n")

# Создаём предмет
subject = Subject.objects.create(
    name="Математика",
    description="Основные темы",
    created_by_id=1
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
    QuestionTemplate.objects.create(
        topic=topic,
        question_type='open',
        text_template=text,
        correct_answer_template=answer,
        points=2
    )

def add_single_question(topic, text, correct, wrong):
    options = [
        {"text": correct, "is_correct": True},
        {"text": wrong, "is_correct": False}
    ]
    QuestionTemplate.objects.create(
        topic=topic,
        question_type='single',
        text_template=text,
        correct_answer_template=correct,
        options_template=options,
        points=2
    )

# ===== 1. Квадратные уравнения (15 шаблонов) =====
topic1 = create_topic("Квадратные уравнения", "ax² + bx + c = 0", 2)
# 8 открытых
for i in range(8):
    a = random.randint(1, 5)
    b = random.randint(-10, 10)
    c = random.randint(-10, 10)
    add_open_question(topic1, f"{a}x² + {b}x + {c} = 0", f"{a}x² + {b}x + {c} = 0")
# 7 тестовых (про дискриминант)
test_questions = [
    ("Дискриминант D = b² - 4ac", "D = b² - 4ac", "D = b² + 4ac"),
    ("Если D > 0, то корней", "два", "один"),
    ("Если D = 0, то корней", "один", "два"),
    ("Если D < 0, то корней", "нет", "один"),
    ("Сумма корней по Виету равна", "-b/a", "b/a"),
    ("Произведение корней по Виету равно", "c/a", "-c/a"),
    ("Формула корней квадратного уравнения", "x = (-b ± √D)/(2a)", "x = (-b ± √D)/a"),
]
for text, correct, wrong in test_questions:
    add_single_question(topic1, text, correct, wrong)
print(f"    Добавлено 8 открытых + 7 тестовых = 15\n")

# ===== 2. Линейные уравнения (15 шаблонов) =====
topic2 = create_topic("Линейные уравнения", "ax + b = 0", 1)
# 8 открытых
for i in range(8):
    a = random.randint(1, 10)
    b = random.randint(-10, 10)
    add_open_question(topic2, f"{a}x + {b} = 0", f"{a}x + {b} = 0")
# 7 тестовых
test_questions2 = [
    ("Уравнение вида ax + b = 0 называется", "линейным", "квадратным"),
    ("Корень уравнения 2x + 6 = 0 равен", "-3", "3"),
    ("Корень уравнения 5x - 10 = 0 равен", "2", "-2"),
    ("Если a = 0 и b = 0, то уравнение", "бесконечно много решений", "не имеет решений"),
    ("Если a = 0 и b ≠ 0, то уравнение", "не имеет решений", "имеет одно решение"),
    ("Формула корня линейного уравнения ax + b = 0", "x = -b/a", "x = b/a"),
    ("Решение уравнения 3x = 12", "4", "36"),
]
for text, correct, wrong in test_questions2:
    add_single_question(topic2, text, correct, wrong)
print(f"    Добавлено 8 открытых + 7 тестовых = 15\n")

# ===== 3. Проценты (15 шаблонов) =====
topic3 = create_topic("Проценты", "Нахождение процента от числа", 2)
# 8 открытых
for i in range(8):
    a = random.randint(10, 200)
    p = random.randint(1, 50)
    add_open_question(topic3, f"Найдите {p}% от числа {a}", f"{a} * {p} / 100")
# 7 тестовых
test_questions3 = [
    ("1% от числа — это", "сотая часть", "десятая часть"),
    ("Чтобы найти 20% от числа, нужно умножить на", "0.2", "0.02"),
    ("Число увеличили на 30%, получили", "в 1.3 раза больше", "в 0.7 раза меньше"),
    ("Число уменьшили на 30%, получили", "в 0.7 раза меньше", "в 1.3 раза больше"),
    ("50% от числа — это", "половина", "четверть"),
    ("25% от числа — это", "четверть", "половина"),
    ("10% от числа — это", "десятая часть", "пятая часть"),
]
for text, correct, wrong in test_questions3:
    add_single_question(topic3, text, correct, wrong)
print(f"    Добавлено 8 открытых + 7 тестовых = 15\n")

# ===== 4. Степени и корни (15 шаблонов) =====
topic4 = create_topic("Степени и корни", "Степени и квадратные корни", 2)
# 8 открытых
for i in range(8):
    a = random.randint(2, 10)
    exp = random.choice([2, 3, 4])
    add_open_question(topic4, f"{a}^{exp}", f"{a}^{exp}")
# 7 тестовых
test_questions4 = [
    ("a² × a³ =", "a⁵", "a⁶"),
    ("a⁵ ÷ a² =", "a³", "a⁷"),
    ("(a²)³ =", "a⁶", "a⁵"),
    ("a⁰ = (a≠0)", "1", "0"),
    ("a⁻² =", "1/a²", "a²"),
    ("√a × √a =", "a", "a²"),
    ("(√a)² =", "a", "|a|"),
]
for text, correct, wrong in test_questions4:
    add_single_question(topic4, text, correct, wrong)
print(f"    Добавлено 8 открытых + 7 тестовых = 15\n")

print("="*60)
print("✅ ГОТОВО! Создано 4 темы, 60 шаблонов (открытые + тестовые).")
print("="*60)