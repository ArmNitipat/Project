from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

# class Post(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()

#     def __str__(self):
#         return self.title



class Bannerslide(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    image = models.ImageField(upload_to='bannerslides/', verbose_name="Image")
    description = models.TextField(blank=True, verbose_name="Description" ,max_length=500)
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
    

class Premium(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name="Title")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Price")
    num = models.PositiveIntegerField(verbose_name="Number")
    # maximum
    imag = models.ImageField(upload_to='premium_images/', verbose_name="Image")
    update_date = models.DateTimeField(auto_now=True,verbose_name="Date")
    expires = models.DateField(verbose_name="Expires")

    class Meta:
        verbose_name = 'Premium iteam'
        verbose_name_plural = 'Premium iteam'

    def delete(self, *args, **kwargs):
        # ลบรูปภาพก่อน
        self.imag.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
         return self.name

from django.db import models


class Premium_list(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    premium = models.ForeignKey(Premium, on_delete=models.CASCADE, verbose_name="Premium Product")
    
    class Meta:
        verbose_name = "Product List"
        verbose_name_plural = "Product Lists"

    def __str__(self):
        return f"{self.user.username} - {self.premium.name}"


# class IPAddress(models.Model):
#     ip = models.GenericIPAddressField(unique=True)
#     count = models.PositiveIntegerField(default=0)

# class movie(models.Model):

# mainActor!!!!!!
class Comment(models.Model):
    SENTIMENT_CHOICES = (
        ('Positive', 'Positive'),
        ('Negative', 'Negative'),
        ('Neutral', 'Neutral'),
    )# การกำหนดคู่ของค่า ค่าเเรกจะเก็บในฐานข้อมูล ค่าที่สองจะแสดงในเว็บ

    data = models.TextField()
    score = models.IntegerField(default=1,validators=[MaxValueValidator(10),MinValueValidator(1)])
    spoiler = models.BooleanField()
    update_date = models.DateTimeField(auto_now=True,verbose_name="Date")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    toplike = models.IntegerField(default=0)
    sentiment = models.CharField(max_length=8, choices=SENTIMENT_CHOICES, default='Neutral')

    def delete(self, *args, **kwargs):
        # Delete related reports
        self.report_set.all().delete()
        # Call the "real" delete() method
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.movie.name}"

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        # ตรวจสอบว่า user และ comment ไม่ซ้ำกัน
        unique_together = ('user', 'comment')

    def __str__(self):
        return f"Like by {self.user.username} on {self.comment.id}"

from django.db.models.deletion import ProtectedError   
class Report(models.Model):
    STATUS = (
        ('waiting', 'Waiting'),
        ('deleted', 'Deleted'),
    )
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS, default='waiting')

    def save(self, *args, **kwargs):
        # ตรวจสอบว่าสถานะเป็น 'ลบแล้ว' และอินสแตนซ์ยังไม่ถูกลบ
        if self.status == 'deleted' and self.pk is not None:
            try:
                comment = self.comment
                self.delete()
                # Now delete the comment, checking if it still exists
                if comment and comment.pk is not None:
                    comment.delete()
            except ProtectedError:
                # ป้องกันการลบ
                # การจัดการ เพิ่มใหม่ (e.g., re-raise or log the error)
                raise
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"Report {self.id} for comment {self.comment.id}"