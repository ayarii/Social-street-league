from django.urls import path , include
from . import views
urlpatterns = [
  path('', views.display,name='team'),
  path('singleteam/<int:id>', views.team_detail,name='singleteam'),
  path('jointeam/<int:id>', views.join_team,name='jointeam'),
]
