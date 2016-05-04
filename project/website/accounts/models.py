from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, blank=True, default='')
    email = models.EmailField(blank=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'mahjong_user'

    def __str__(self):
        return self.email

    def get_short_name(self):
        pass

    def get_full_name(self):
        pass


class Player(models.Model):
    user = models.ForeignKey(User, related_name='players')
    username = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mahjong_player'

    def __str__(self):
        return self.username


def user_created(sender, instance, created, **kwargs):
    if created:
        from api.models import ApiToken
        ApiToken.objects.create(user=instance)

post_save.connect(user_created, sender=User)
