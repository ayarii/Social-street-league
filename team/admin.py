from django.contrib import admin

from team.models import Team

from users.models import Joined_team

# Register your models here.
class joined_team(admin.TabularInline):
    model=Joined_team
    extra= 1

@admin.register(Team)
class Team_admin(admin.ModelAdmin):
    inlines= [joined_team]
    
# admin.site.register(Team,joined_team)
