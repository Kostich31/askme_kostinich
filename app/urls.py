from django.urls import path

from app import views

app_urlpatterns = [
    path('ask/', views.ask, name='ask'),
    path('login/', views.login, name='login'),
    path('question/<int:pk>/', views.question, name='one_question'),
    path('signup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('hot/', views.hot, name='hot'),
    path('tag/<tag>/', views.tag, name='tag'),
    path('', views.index, name='index')
]
