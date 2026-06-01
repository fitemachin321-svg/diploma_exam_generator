from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from .models import Subject, Topic, GeneratedWork, QuestionTemplate
from .pdf_generator import ExamPDFGenerator
from .docx_generator import ExamDOCXGenerator
from .utils import parse_template, generate_random_value, substitute_variables, generate_math_answer, generate_auto_test_question
import json
import os
import random
from datetime import datetime, timedelta

def index(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    works = GeneratedWork.objects.filter(created_by=request.user).order_by('-created_at')
    
    # Поиск по названию
    search_query = request.GET.get('search', '')
    if search_query:
        works = works.filter(title__icontains=search_query)
    
    # Фильтр по предмету
    subject_filter = request.GET.get('subject', '')
    if subject_filter and subject_filter != 'all':
        works = works.filter(subject_id=subject_filter)
    
    # Фильтр по дате
    date_filter = request.GET.get('date_filter', '')
    today = datetime.now().date()
    
    if date_filter == 'today':
        works = works.filter(created_at__date=today)
    elif date_filter == 'week':
        week_ago = today - timedelta(days=7)
        works = works.filter(created_at__date__gte=week_ago)
    elif date_filter == 'month':
        month_ago = today - timedelta(days=30)
        works = works.filter(created_at__date__gte=month_ago)
    
    subjects = Subject.objects.all()
    
    context = {
        'works': works,
        'subjects': subjects,
        'search_query': search_query,
        'subject_filter': subject_filter,
        'date_filter': date_filter,
    }
    return render(request, 'dashboard.html', context)

@login_required
def generate_form(request):
    subjects = Subject.objects.all()
    return render(request, 'generate_form.html', {'subjects': subjects})

def get_topics(request, subject_id):
    topics = Topic.objects.filter(subject_id=subject_id).values('id', 'title', 'difficulty_level')
    return JsonResponse(list(topics), safe=False)

@login_required
def generate_work(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            subject = Subject.objects.get(id=data['subject_id'])
            work = GeneratedWork.objects.create(
                title=data['title'],
                subject=subject,
                variant_count=data['variant_count'],
                created_by=request.user
            )
            work.topics.set(data['topics'])
            questions = list(QuestionTemplate.objects.filter(topic_id__in=data['topics']))
            
            if len(questions) == 0:
                return JsonResponse({'status': 'error', 'message': 'Нет шаблонов вопросов для выбранных тем'}, status=400)
            
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
                        var_answers.append(correct_answer)
                    else:
                        question_text = substitute_variables(q.text_template, vars_dict)
                        answer_text = generate_math_answer(q.text_template, vars_dict)
                        var_questions.append({'text': question_text, 'points': q.points})
                        var_answers.append(answer_text)
                
                all_questions.append(var_questions)
                all_answers[v] = var_answers
            
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'works'), exist_ok=True)
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'answers'), exist_ok=True)
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'docx'), exist_ok=True)
            
            pdf_path = os.path.join(settings.MEDIA_ROOT, 'works', f"work_{work.id}.pdf")
            pdf_gen = ExamPDFGenerator(pdf_path, work.title)
            pdf_gen.generate_header()
            for i, qs in enumerate(all_questions, 1):
                pdf_gen.add_variant(i, qs)
            pdf_gen.build()
            
            ans_path = os.path.join(settings.MEDIA_ROOT, 'answers', f"answers_{work.id}.pdf")
            ans_gen = ExamPDFGenerator(ans_path, f"Ответы: {work.title}")
            ans_gen.generate_header()
            ans_gen.generate_answers(all_answers)
            ans_gen.build()
            
            docx_path = os.path.join(settings.MEDIA_ROOT, 'docx', f"work_{work.id}.docx")
            docx_gen = ExamDOCXGenerator(docx_path, work.title)
            docx_gen.generate_header()
            for i, qs in enumerate(all_questions, 1):
                docx_gen.add_variant(i, qs)
            docx_gen.build()
            
            work.pdf_file = f'works/work_{work.id}.pdf'
            work.answers_file = f'answers/answers_{work.id}.pdf'
            work.docx_file = f'docx/work_{work.id}.docx'
            work.save()
            
            return JsonResponse({
                'status': 'ok',
                'message': 'Работа успешно создана',
                'docx_url': f'/media/docx/work_{work.id}.docx'
            })
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'}, status=405)

@login_required
def delete_work(request, work_id):
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
        if work.docx_file:
            path = os.path.join(settings.MEDIA_ROOT, str(work.docx_file))
            if os.path.exists(path):
                os.remove(path)
        work.delete()
        return JsonResponse({'status': 'ok', 'message': 'Работа удалена'})
    except GeneratedWork.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Работа не найдена'}, status=404)