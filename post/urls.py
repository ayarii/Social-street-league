from django.urls import path , include
from . import views
urlpatterns = [
   path('', views.display,name='post'),
   path('addpost/', views.add_post,name='addpost'),
   path('updatepost/<int:id>', views.update_post,name='updatepost'),
   path('deletepost/<int:id>', views.delete_post,name='deletepost'),
]
