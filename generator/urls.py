from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    # Веб-маршруты
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('generate/', views.generate_form, name='generate_form'),
    path('generate/create/', views.generate_work, name='generate_work'),
    path('get-topics/<int:subject_id>/', views.get_topics, name='get_topics'),
    path('delete-work/<uuid:work_id>/', views.delete_work, name='delete_work'),
    
    # API маршруты
    path('api/subjects/', api_views.subjects_list, name='api_subjects'),
    path('api/topics/<int:subject_id>/', api_views.topics_list, name='api_topics'),
    path('api/questions/<int:topic_id>/', api_views.questions_list, name='api_questions'),
    path('api/generate/', api_views.api_generate_work, name='api_generate'),
    path('api/works/', api_views.user_works, name='api_works'),
    path('api/delete-work/<uuid:work_id>/', api_views.delete_work_api, name='api_delete_work'),
]