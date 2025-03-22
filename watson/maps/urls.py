from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Watson UQ'),
    path('list/', views.course_list, name='Watson UQ')
]