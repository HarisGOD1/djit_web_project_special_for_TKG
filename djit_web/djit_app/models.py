from django.db import models

# Create your models here.

from django.db import models

class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  phone = models.IntegerField()
  joined_date = models.DateField()


# to-do repo class
# to-do incude users in it

