from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from users.models import Disponibility, User,Banned_User
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

def ban_users(self,request, queryset):
    queryset.update(is_active = False)
    banned_user = Banned_User.objects.create(User=request.user,banned_reason="")
    for obj in queryset:
        if hasattr(obj,'user'):
            obj=obj.user
        current_site = get_current_site(request)
        text_content=render_to_string("banned_email.html",{"user":obj,"domain":current_site.domain}).strip()
        email = EmailMultiAlternatives(
			#subject
			"Your account was banned",
			#content
			text_content,
			#from email,
			settings.EMAIL_HOST_USER,
			#to list
			[obj.email]
		)
        email.content_subtype = 'html'
        email.mixed_subtype = 'related'
        email.send()
    banned_user.save()
    self.message_user(request, "User banned")
    
def remove_ban(self, request, queryset):
    print(queryset)
    for obj in queryset:
        if hasattr(obj,'user'):
            obj=obj.user
        current_site = get_current_site(request)
        text_content=render_to_string("unbanned_email.html",{"user":obj,"domain":current_site.domain}).strip()
        email = EmailMultiAlternatives(
			#subject
			"Welcome Back !",
			#content
			text_content,
			#from email,
			settings.EMAIL_HOST_USER,
			#to list
			[obj.email]
		)
        email.content_subtype = 'html'
        email.mixed_subtype = 'related'
        email.send()
    queryset.update(is_active = True)
    self.message_user(request, "Users ban has been lifted")

class AccountAdmin(UserAdmin):
	list_display = ('email','username','date_joined', 'last_login', 'is_admin','is_active',)
	search_fields = ('email','username',)
	readonly_fields=('id', 'date_joined', 'last_login','email','username','profile_image','birth_date','user_disponibility','address','prefer_activity','password',)

	actions = [ban_users, remove_ban]
	
	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.register(User,AccountAdmin)
admin.site.register(Disponibility)

admin.site.unregister(Group)