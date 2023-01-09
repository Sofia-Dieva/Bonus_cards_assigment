from django.urls import path
from . import views

urlpatterns = [
    path('', views.Check_is_active, name='all'),
    path('search/', views.SearchCard, name='search'),
    path('generate/', views.GenerateCard, name='generate'),
    path('card/<int:pk>/', views.CardDetail.as_view(), name='card'),
]
