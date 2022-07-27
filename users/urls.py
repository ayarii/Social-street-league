from django.urls import path , include
from . import views
urlpatterns = [
    path('login/', views.login_user,name='login'),
    path('signup/', views.signup_user,name='signup'),
    path('logout/<int:id>', views.logout_user,name='logout'),
    path('profile/<int:id>', views.profile_user,name='profile'),
    path('updateprofile/<int:id>', views.profile_update,name='updateprofile'),
    path('', views.user,name='users'),
 
]
