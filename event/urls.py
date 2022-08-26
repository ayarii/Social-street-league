from django.urls import path , include
from . import views
urlpatterns = [
  path('', views.list_event,name='event'),
  path('even/<int:id>', views.even, name = 'even'),
  path('addevent/', views.addev, name='addev'),
]
