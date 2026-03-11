from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('',                     views.recipe_list,   name='recipe_list'),
    path('new/',                 views.recipe_create, name='recipe_create'),
    path('<int:pk>/',            views.recipe_detail, name='recipe_detail'),
    path('<int:pk>/edit/',       views.recipe_edit,   name='recipe_edit'),
]
