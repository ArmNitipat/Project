from django.db import models
from django.core.exceptions import ValidationError

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
  
  # class User(models.Model):
  #   # ... ส่วนอื่นๆ ของ model ของคุณ ...
  #   date_of_birth = models.DateField(null=True, blank=True)


class Bannerslide(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    image = models.ImageField(upload_to='bannerslides/', verbose_name="Image")
    description = models.TextField(blank=True, verbose_name="Description")
    active = models.BooleanField(default=True, verbose_name="Is Active")
    order = models.PositiveIntegerField(default=0, verbose_name="Order")
    
    class Meta:
        ordering = ['order',]
        verbose_name = 'Banner Slide'
        verbose_name_plural = 'Banner Slides'

    def delete(self, *args, **kwargs):
      # ลบรูปภาพก่อน
      self.image.delete()
      super().delete(*args, **kwargs)  

    def __str__(self):
        return self.title

# class IPAddress(models.Model):
#     ip = models.GenericIPAddressField(unique=True)
#     count = models.PositiveIntegerField(default=0)


