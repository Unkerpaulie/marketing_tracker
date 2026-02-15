from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('ads/', views.ads_list, name='ads_list'),
    path('ads/create/', views.create_ad, name='create_ad'),
    path('add-post/<int:group_id>/', views.add_post, name='add_post'),
]

