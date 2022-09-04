from django.urls import path , include
from . import views
urlpatterns = [
  path('', views.list_event,name='event'),
  path('even/<int:id>', views.even, name = 'even'),
  path('addevent/', views.addev, name='addev'),
  path('event_pdf/', views.event_pdf, name='event_pdf'),
  path('contact/', views.contact, name='contact'),
  path('updatev/<int:id>', views.updatev, name = 'updatev'),
  path('eve/', views.eve, name='eve'),
]


