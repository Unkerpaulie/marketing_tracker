from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('test-lexical/', views.test_lexical, name='test_lexical'),
]
