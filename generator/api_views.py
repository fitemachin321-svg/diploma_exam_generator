from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Subject, Topic, QuestionTemplate, GeneratedWork
from .serializers import SubjectSerializer, TopicSerializer, QuestionTemplateSerializer, GeneratedWorkSerializer, GenerateWorkSerializer
from .utils import parse_template, generate_random_value, substitute_variables, generate_math_answer, generate_auto_test_question
from .pdf_generator import ExamPDFGenerator
import os
import random
import json

@api_view(['GET'])
def subjects_list(request):
    """Список всех предметов"""
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def topics_list(request, subject_id):
    """Список тем по ID предмета"""
    topics = Topic.objects.filter(subject_id=subject_id)
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def questions_list(request, topic_id):
    """Список шаблонов вопросов по ID темы"""
    questions = QuestionTemplate.objects.filter(topic_id=topic_id)
    serializer = QuestionTemplateSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_generate_work(request):
    """API для генерации работы"""
    serializer = GenerateWorkSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    
    try:
        subject = Subject.objects.get(id=data['subject_id'])
        work = GeneratedWork.objects.create(
            title=data['title'],
            work_type=data['work_type'],
            subject=subject,
            variant_count=data['variant_count'],
            created_by=request.user
        )
        work.topics.set(data['topics'])
        questions = list(QuestionTemplate.objects.filter(topic_id__in=data['topics']))
        
        if len(questions) == 0:
            return Response({'error': 'Нет шаблонов вопросов для выбранных тем'}, status=status.HTTP_400_BAD_REQUEST)
        
        work_type_display = dict(GeneratedWork.WORK_TYPES).get(data['work_type'], 'Работа')
        all_questions = []
        all_answers = {}
        
        tasks_count = data.get('tasks_count', 5)
        variant_count = data.get('variant_count', 4)
        
        for v in range(1, variant_count + 1):
            selected = random.sample(questions, min(tasks_count, len(questions)))
            random.shuffle(selected)
            var_questions = []
            var_answers = []
            
            for q in selected:
                vars_dict = {}
                for var in parse_template(q.text_template):
                    vars_dict[var] = generate_random_value(var)
                
                if q.question_type == 'single':
                    full_question, correct_answer = generate_auto_test_question(q, vars_dict)
                    var_questions.append({'text': full_question, 'points': q.points})
                    var_answers.append(f"Правильный ответ: {correct_answer}")
                else:
                    question_text = substitute_variables(q.text_template, vars_dict)
                    answer_text = generate_math_answer(q.text_template, vars_dict)
                    var_questions.append({'text': question_text, 'points': q.points})
                    var_answers.append(answer_text)
            
            all_questions.append(var_questions)
            all_answers[v] = var_answers
        
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'works'), exist_ok=True)
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'answers'), exist_ok=True)
        
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'works', f"work_{work.id}.pdf")
        pdf_gen = ExamPDFGenerator(pdf_path, work.title, work_type_display)
        pdf_gen.generate_header()
        for i, qs in enumerate(all_questions, 1):
            pdf_gen.add_variant(i, qs)
        pdf_gen.build()
        
        ans_path = os.path.join(settings.MEDIA_ROOT, 'answers', f"answers_{work.id}.pdf")
        ans_gen = ExamPDFGenerator(ans_path, f"Ответы: {work.title}", work_type_display)
        ans_gen.generate_header()
        ans_gen.generate_answers(all_answers)
        ans_gen.build()
        
        work.pdf_file = f'works/work_{work.id}.pdf'
        work.answers_file = f'answers/answers_{work.id}.pdf'
        work.save()
        
        return Response({
            'success': True,
            'work_id': str(work.id),
            'pdf_url': work.pdf_file.url if work.pdf_file else None,
            'answers_url': work.answers_file.url if work.answers_file else None
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_works(request):
    """Список работ текущего пользователя"""
    works = GeneratedWork.objects.filter(created_by=request.user).order_by('-created_at')
    serializer = GeneratedWorkSerializer(works, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_work_api(request, work_id):
    """Удаление работы через API"""
    try:
        work = GeneratedWork.objects.get(id=work_id, created_by=request.user)
        if work.pdf_file:
            path = os.path.join(settings.MEDIA_ROOT, str(work.pdf_file))
            if os.path.exists(path):
                os.remove(path)
        if work.answers_file:
            path = os.path.join(settings.MEDIA_ROOT, str(work.answers_file))
            if os.path.exists(path):
                os.remove(path)
        work.delete()
        return Response({'success': True, 'message': 'Работа удалена'})
    except GeneratedWork.DoesNotExist:
        return Response({'error': 'Работа не найдена'}, status=status.HTTP_404_NOT_FOUND)