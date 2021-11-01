from django.conf.urls import re_path
from toys import views
from django.urls import path


urlpatterns = [
    path('', views.toy_list, name='toys_list'),
    path('<int:pk>/', views.toy_detail, name='toy_detail'),
]
