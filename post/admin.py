from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 

from post.models import Post ,Post_Participants

# Register your models here.

class PostAdmin(admin.ModelAdmin):
	list_display = ('post_title','created_at','user',)
	search_fields = ('post_title','user',)
	#readonly_fields=('id', 'date_joined', 'last_login','email','username','profile_image','birth_date','user_disponibility','address','prefer_activity','password','user_events')
	readonly_fields=('created_at', 'updated_at')
	filter_horizontal = ()
	list_filter = ()
	fieldsets = (
               (None,{'fields':('post_title','post_description','post_date','post_location','post_image','tags','user')}),
              ('Important dates', {'fields': ('created_at', 'updated_at')}),
              )

admin.site.register(Post,PostAdmin)

