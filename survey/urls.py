from django.urls import path
from . import views
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.conf import settings

app_name = 'survey'

urlpatterns = [
    path('', views.survey_list, name="survey_list"),
    path('<int:pk>/', views.survey_detail, name="survey_detail"),
    path('new/', views.survey_new, name="survey_new"),
    path('<int:pk>/comments/new2/', views.comment_new2, name="comment_new2"),
    path('<int:pk>/comments/edit/<int:pk2>/', views.comment_edit, name="comment_edit"),
    path('<int:pk>/post_delete/', views.post_delete, name="post_delete"),
    path('<int:pk>/comment_delete/<int:pk2>/', views.comment_delete, name="comment_delete"),
    path('calculate/', views.calculate, name="calculate"),
    path('calculate/withdraw/', views.withdraw, name="withdraw"),
    path('calculate/deposit/', views.deposit, name="deposit"),
    path('update/', views.update, name="update"),
    path('my_survey/', views.my_survey, name="my_survey"),
    path('my_comment/', views.my_comment, name="my_comment"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
