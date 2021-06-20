from django.db import models

# Create your models here.
class User(models.Model):
    """ user information shown """
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=20)
    phone_number=models.IntegerField()
    address=models.CharField(max_length=100)

    def __str__(self):
        return self.username

