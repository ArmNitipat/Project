from django.db import models

# Create your models here.

# class Post(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()

#     def __str__(self):
#         return self.title

class myuser(models.Model):
  username = models.CharField(max_length=15, primary_key=True)
  password = models.CharField(max_length=15)
  firstname = models.CharField(max_length=20)
  lastname = models.CharField(max_length=20)
  date_of_birth = models.DateField()
  email = models.EmailField()

  def __str__(self):
    return f"{self.firstname} {self.lastname}"
  
  class User(models.Model):
    # ... ส่วนอื่นๆ ของ model ของคุณ ...
    date_of_birth = models.DateField(null=True, blank=True)

# from django.db import models

# class IPAddress(models.Model):
#     ip = models.GenericIPAddressField(unique=True)
#     count = models.PositiveIntegerField(default=0)