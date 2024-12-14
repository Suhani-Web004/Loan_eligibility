from django.db import models

# Create your models here.
class NewUser(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    email = models.EmailField(null=False, unique=True)
    password = models.CharField(null=False, max_length=128)

    def __str__(self):
        return self.username