from django.db import models

# Create your models here.
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

class Repository(models.Model):
  repository_name = models.CharField(max_length=255)
  repository_description = models.CharField(max_length=511)
  repository_privacy = models.BooleanField() # true - private false - public


  owner_name = models.CharField(max_length=255)
  members_name = ArrayField(models.CharField(max_length=255), blank=True)
  # Repository.objects.create(repository_name='First post', members_name=['thoughts', 'django'])




class DjitUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255)
    repositories = models.ManyToManyField(Repository)

