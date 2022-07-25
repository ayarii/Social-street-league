from django.urls import path , include
from . import views
urlpatterns = [
    path('login/', views.login_user,name='login'),
    path('signup/', views.signup_user,name='signup'),
    path('logout/<int:id>', views.logout_user,name='logout'),
    path('', views.user,name='users'),
 
]
