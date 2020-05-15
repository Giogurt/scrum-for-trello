from django.urls import path

from . import views


app_name = 'scrum'
urlpatterns = {
    #ex: /scrum/
    path('', views.index, name='index'),
    path('etapa/<str:list_name>/', views.etapa, name='etapa'),
    path('member/<str:member_name>/', views.member, name='member')
}