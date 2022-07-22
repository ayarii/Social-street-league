from django.urls import path , include
from . import views
urlpatterns = [
    path('login/', views.login_user,name='login'),
    path('signup/', views.signup_user,name='signup'),
    path('', views.user,name='users'),
 
]
