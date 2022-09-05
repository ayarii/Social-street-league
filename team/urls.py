from django.urls import path , include
from . import views
urlpatterns = [
  path('', views.display, name='team'),
  path('singleteam/<int:id>', views.team_detail,name='singleteam'),
  path('jointeam/<int:id>', views.join_team,name='jointeam'),
  path('leaveteam/<int:id>', views.leave_team,name='leaveteam'),
  path('Search_ajax', views.Search_ajax,name='Search_ajax'),
]
