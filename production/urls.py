from django.urls import path
from . import views

app_name = 'production'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('batches/', views.batch_list, name='batch_list'),
    path('batches/new/', views.batch_create, name='batch_create'),
    path('batches/<int:pk>/', views.batch_detail, name='batch_detail'),
    path('batches/<int:pk>/update-status/', views.batch_update_status, name='batch_update_status'),
]
