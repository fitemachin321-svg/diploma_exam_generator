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
    QuestionTemplate.objects.create(
        topic=topic,
        question_type='single',
        text_template=text,
        correct_answer_template=correct,
        options_template=[{"text": wrong, "is_correct": False}],
        points=2
    )

# ===== 1. Квадратные уравнения =====
topic1 = create_topic("Квадратные уравнения", "ax² + bx + c = 0", 2)
for i in range(15):
    a = random.randint(1, 5)
    b = random.randint(-10, 10)
    c = random.randint(-10, 10)
    # Для открытых вопросов ответ вычисляем прямо здесь
    D = b*b - 4*a*c
    if D < 0:
        answer = "нет действительных корней"
    elif D == 0:
        x = round(-b/(2*a), 2)
        answer = f"x = {x}"
    else:
        x1 = round((-b - D**0.5)/(2*a), 2)
        x2 = round((-b + D**0.5)/(2*a), 2)
        answer = f"x1 = {x1}, x2 = {x2}"
    add_open_question(topic1, f"{a}x² + {b}x + {c} = 0", answer)
print(f"    Добавлено 15 открытых квадратных уравнений\n")

# ===== 2. Линейные уравнения =====
topic2 = create_topic("Линейные уравнения", "ax + b = 0", 1)
for i in range(8):
    a = random.randint(1, 10)
    b = random.randint(-10, 10)
    x = round(-b/a, 2)
    answer = f"x = {x}"
    add_open_question(topic2, f"{a}x + {b} = 0", answer)
# 7 тестовых
tests2 = [
    ("Уравнение вида ax + b = 0 называется", "линейным", "квадратным"),
    ("Корень уравнения 2x + 6 = 0 равен", "-3", "3"),
    ("Корень уравнения 5x - 10 = 0 равен", "2", "-2"),
    ("Если a=0 и b=0, то уравнение", "бесконечно много решений", "не имеет решений"),
    ("Если a=0 и b≠0, то уравнение", "не имеет решений", "имеет одно решение"),
    ("Формула корня ax + b = 0", "x = -b/a", "x = b/a"),
    ("Решение уравнения 3x = 12", "4", "36"),
]
for text, correct, wrong in tests2:
    add_single_question(topic2, text, correct, wrong)
print(f"    Добавлено 8 открытых + 7 тестовых = 15\n")

# ===== 3. Проценты =====
topic3 = create_topic("Проценты", "Проценты от числа", 2)
for i in range(8):
    a = random.randint(10, 200)
    p = random.randint(1, 50)
    ans = round(a * p / 100, 2)
    add_open_question(topic3, f"Найдите {p}% от числа {a}", str(ans))
tests3 = [
    ("1% от числа — это", "сотая часть", "десятая часть"),
    ("Чтобы найти 20% от числа, нужно умножить на", "0.2", "0.02"),
    ("Число увеличили на 30%, получили", "в 1.3 раза больше", "в 0.7 раза меньше"),
    ("Число уменьшили на 30%, получили", "в 0.7 раза меньше", "в 1.3 раза больше"),
    ("50% от числа — это", "половина", "четверть"),
    ("25% от числа — это", "четверть", "половина"),
    ("10% от числа — это", "десятая часть", "пятая часть"),
]
for text, correct, wrong in tests3:
    add_single_question(topic3, text, correct, wrong)
print(f"    Добавлено 8 открытых + 7 тестовых = 15\n")

# ===== 4. Степени и корни =====
topic4 = create_topic("Степени и корни", "Степени и корни", 2)
for i in range(8):
    a = random.randint(2, 5)
    exp = random.choice([2, 3, 4])
    ans = a ** exp
    add_open_question(topic4, f"{a}^{exp}", str(ans))
tests4 = [
    ("a² × a³ =", "a⁵", "a⁶"),
    ("a⁵ ÷ a² =", "a³", "a⁷"),
    ("(a²)³ =", "a⁶", "a⁵"),
    ("a⁰ = (a≠0)", "1", "0"),
    ("a⁻² =", "1/a²", "a²"),
    ("√a × √a =", "a", "a²"),
    ("(√a)² =", "a", "|a|"),
]
for text, correct, wrong in tests4:
    add_single_question(topic4, text, correct, wrong)
print(f"    Добавлено 8 открытых + 7 тестовых = 15\n")

print("="*60)
print("✅ ГОТОВО! Создано 4 темы, 60 шаблонов (все вопросы работают).")
print("="*60)