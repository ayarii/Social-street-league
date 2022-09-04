from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from activity.models import Activity
from event.models import Event
from dateutil.relativedelta import relativedelta
from team.models import Team


# Create your models here.

class Disponibility(models.Model):
    disponibility_name=models.CharField(max_length=50,null=True, blank=False)
    def __str__(self):
        return self.disponibility_name
    
class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined	= models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_login= models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, upload_to='users_photo', null=True, blank=True, default='users_photo/default_user.jpg')
    birth_date= models.DateField(null=True, blank=False)
    user_disponibility=models.ManyToManyField(Disponibility)
    address = models.CharField(max_length=50,null=True, blank=False)
    lat = models.CharField(max_length=256,null=True,blank=True)
    long = models.CharField(max_length=256,null=True,blank=True)
    prefer_activity = models.ManyToManyField(Activity)
    user_events = models.ManyToManyField(Event)
    team_users = models.ManyToManyField(Team,related_name='users',through='users.Joined_team',blank=True,)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = MyAccountManager()
    
    def __str__(self):
        return self.username
    # For checking permissions. to keep it simple all admin have ALL permissons
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
    
    def user_age(self):
        today = date.today()
        delta = relativedelta(today,self.birth_date)
        return str(delta.years)
    class Meta:
        app_label='users'
        db_table='user'
    
class Joined_team(models.Model):
    user= models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    team= models.ForeignKey(
        to=Team,
        on_delete=models.CASCADE
    )
    date_joined=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_approved= models.BooleanField(default=False)
    
    class Meta:
        app_label= 'users'
        db_table= 'users_user_user_teams'
        
    def __str__(self):
          return f'{self.user} {self.team}'

class Banned_User(models.Model):
    def __str__(self):
        return self.user.username

    User = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        related_name='banned_profile'
    )

    banned_reason = models.TextField(max_length=1000)

    date_banned = models.DateField(auto_now_add=True, null=True, blank=True)
    
    

    