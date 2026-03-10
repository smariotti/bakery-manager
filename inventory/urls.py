from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('products/new/', views.product_create, name='product_create'),
    path('ingredients/', views.ingredient_list, name='ingredient_list'),
    path('ingredients/new/', views.ingredient_create, name='ingredient_create'),
]
