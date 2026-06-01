from django.db import models
from django.contrib.auth.models import User
import uuid

class Subject(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Создатель")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
    
    def __str__(self):
        return self.name

class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics', verbose_name="Предмет")
    title = models.CharField(max_length=300, verbose_name="Название темы")
    content = models.TextField(verbose_name="Содержание")
    difficulty_level = models.IntegerField(
        choices=[(1, 'Легкий'), (2, 'Средний'), (3, 'Сложный')],
        default=2,
        verbose_name="Уровень сложности"
    )
    
    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"
    
    def __str__(self):
        return f"{self.subject.name} - {self.title}"

class QuestionTemplate(models.Model):
    QUESTION_TYPES = [
        ('single', 'Выбор одного варианта'),
        ('open', 'Открытый вопрос'),
    ]
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='questions', verbose_name="Тема")
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, verbose_name="Тип вопроса")
    text_template = models.TextField(verbose_name="Текст вопроса")
    correct_answer_template = models.CharField(max_length=500, blank=True, verbose_name="Шаблон ответа")
    options_template = models.JSONField(null=True, blank=True, verbose_name="Варианты ответов")
    points = models.IntegerField(default=1, verbose_name="Баллы")
    
    class Meta:
        verbose_name = "Шаблон вопроса"
        verbose_name_plural = "Шаблоны вопросов"
    
    def __str__(self):
        return f"{self.topic.title[:50]}..."

class GeneratedWork(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300, verbose_name="Название")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    topics = models.ManyToManyField(Topic, verbose_name="Темы")
    variant_count = models.IntegerField(default=4, verbose_name="Количество вариантов")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Создатель")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    pdf_file = models.FileField(upload_to='works/', null=True, blank=True, verbose_name="PDF файл")
    answers_file = models.FileField(upload_to='answers/', null=True, blank=True, verbose_name="PDF с ответами")
    docx_file = models.FileField(upload_to='docx/', null=True, blank=True, verbose_name="DOCX файл")
    
    class Meta:
        verbose_name = "Сгенерированная работа"
        verbose_name_plural = "Сгенерированные работы"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.created_at.strftime('%d.%m.%Y')})"