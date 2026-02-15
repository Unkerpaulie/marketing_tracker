from django.urls import path
from . import views

app_name = 'engagement'

urlpatterns = [
    path('post/<int:post_id>/', views.view_engagements, name='view_engagements'),
    path('post/<int:post_id>/add/', views.add_engagement, name='add_engagement'),
    path('contacts/', views.contacts_list, name='contacts_list'),
    path('contacts/create/', views.create_contact, name='create_contact'),
]

