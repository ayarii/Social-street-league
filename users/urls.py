from django.urls import path , include
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login/', views.login_user,name='login'),
    path('signup/', views.signup_user,name='signup'),
    path('logout/<int:id>', views.logout_user,name='logout'),
    path('profile/<int:id>', views.profile_user,name='profile'),
    #path('updateprofile/<int:id>', views.profile_update,name='updateprofile'),
    path('filter-data',views.filter_data,name='filter_data'),
    path('load-more-data-post',views.load_more_data_post,name='load_more_data-post'),
    path('load-more-data-event',views.load_more_data_event,name='load_more_data-event'),
    path('load-more-data-team',views.load_more_data_team,name='load_more_data-team'),
    path('profile/<int:id>/cropImage', views.upload_image, name='crop_image'),
    path('activate/<uidb64>/<token>', views.VerificationView.as_view() , name='activate'),
    path('', views.user,name='users'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_form.html'), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset_form.html'), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
     name='password_reset_complete'),
 
]

