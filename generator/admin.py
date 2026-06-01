from django.contrib import admin
from .models import Subject, Topic, QuestionTemplate, GeneratedWork

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    search_fields = ('name',)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'difficulty_level')
    list_filter = ('subject', 'difficulty_level')
    search_fields = ('title',)

@admin.register(QuestionTemplate)
class QuestionTemplateAdmin(admin.ModelAdmin):
    list_display = ('topic', 'question_type', 'points')
    list_filter = ('topic__subject', 'question_type')

@admin.register(GeneratedWork)
class GeneratedWorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'variant_count', 'created_by', 'created_at')
    list_filter = ('subject',)
    search_fields = ('title',)