from django.db import models

# Create your models here.

# class Post(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()

#     def __str__(self):
#         return self.title

class Member(models.Model):
  firstname = models.CharField(max_length=30)
  lastname = models.CharField(max_length=30)
  age = models.IntegerField(max_length=100)
  phone = models.IntegerField(null=True)
  joined_date = models.DateField(auto_now_add=True)

  def __str__(self):
    return f"{self.firstname} {self.lastname}"