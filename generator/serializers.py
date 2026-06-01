from rest_framework import serializers
from .models import Subject, Topic, QuestionTemplate, GeneratedWork

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'created_at']

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title', 'subject', 'difficulty_level', 'content']

class QuestionTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionTemplate
        fields = ['id', 'topic', 'question_type', 'text_template', 'correct_answer_template', 'points']

class GeneratedWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedWork
        fields = ['id', 'title', 'work_type', 'subject', 'variant_count', 'created_at', 'pdf_file', 'answers_file']

class GenerateWorkSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=300)
    subject_id = serializers.IntegerField()
    topics = serializers.ListField(child=serializers.IntegerField())
    work_type = serializers.ChoiceField(choices=['test', 'independent', 'homework'])
    variant_count = serializers.IntegerField(min_value=2, max_value=8)
    tasks_count = serializers.IntegerField(min_value=1, max_value=15)