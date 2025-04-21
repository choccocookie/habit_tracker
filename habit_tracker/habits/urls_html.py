from django.urls import path
from . import views_html


urlpatterns = [
    path('', views_html.habit_list, name='habit_list'),
    path('create/', views_html.habit_create, name='habit_create'),
    path('<int:pk>/edit/', views_html.habit_update, name='habit_update'),
    path('<int:pk>/delete/', views_html.habit_delete, name='habit_delete'),
]
