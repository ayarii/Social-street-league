from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User



class AccountAdmin(UserAdmin):
	list_display = ('email','username','date_joined', 'last_login', 'is_admin','is_staff')
	search_fields = ('email','username',)
	readonly_fields=('id', 'date_joined', 'last_login','email','username','profile_image','age','disponibility','address','user_teams','prefer_activity','user_events','password',)

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.register(User,AccountAdmin)