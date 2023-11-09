from django.db import models

# Create your models here.

# mainActor!!!!!!
# class StarType (models.Model):
#     name = models.CharField(max_length=20)

#     def __str__(self):
#       return self.name

# class Star(models.Model): 
#     name = models.CharField(max_length=100) 
#     # star_type = models.ForeignKey(StarType, on_delete=models.CASCADE)
#     job = models.ManyToManyField(StarType, related_name='stars', blank=True)
#     history = models.TextField(blank=True,null=False)
#     height = models.FloatField(null=False, blank=True,default=0,help_text="height in meters.")
#     born_date = models.DateField(null=True, blank=True)
#     born_location = models.CharField(null=True, blank=True,max_length=255)
#     died_date = models.DateField(null=True, blank=True)
#     died_location = models.CharField(null=True, blank=True,max_length=255)
#     update_time = models.DateTimeField(auto_now=True)
#     active = models.BooleanField(default=True)
      
#     def divmod(value, arg):
#         quotient, remainder = divmod(value, arg)
#         return f"{int(quotient)}'{remainder}\""
      
#     def __str__(self):
#         return self.name

# class Official_sites(models.Model):
#     star = models.ForeignKey(Star, on_delete=models.CASCADE)
#     name_site = models.CharField(null=False,max_length=100) 
#     Official_sites = models.URLField(null=False,max_length=2000)

#     def __str__(self):
#         return f"I for {self.star.name}"

# class StarImage(models.Model):
#     star = models.ForeignKey(Star, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='stars/')
#     mainimage = models.BooleanField(default=False, verbose_name="Is Main")
#     active = models.BooleanField(default=True, verbose_name="Is Active")
    
#     def __str__(self):
#         return f"Image for {self.star.name}"

# class StarImageURL(models.Model):
#     star = models.ForeignKey(Star, on_delete=models.CASCADE)
#     image_url = models.URLField(max_length=2000)
#     active = models.BooleanField(default=True, verbose_name="Is Active")

#     def __str__(self):
#         return f"Image for {self.star.name}"

# class AlternativeNames(models.Model):
#     star = models.ForeignKey(Star, on_delete=models.CASCADE)
#     alternative_name = models.CharField(max_length=100)

# class Spouses(models.Model):
#     star = models.ForeignKey(Star, on_delete=models.CASCADE)
#     spouse = models.ForeignKey(Star, on_delete=models.SET_NULL, null=True, related_name='spouse_star')
#     marriage_date = models.DateField()
#     divorce = models.BooleanField(default=False) 

# class Children(models.Model):
#     star = models.ForeignKey(Star, on_delete=models.CASCADE)
#     child_name = models.ForeignKey(Star, on_delete=models.SET_NULL, null=True, related_name='children_star')

# class Parents(models.Model):
#     star = models.ForeignKey(Star, on_delete=models.CASCADE)
#     Parents_name = models.ForeignKey(Star, on_delete=models.SET_NULL, null=True, related_name='Parents_star')


# class Relatives(models.Model):
#     star = models.ForeignKey(Star, on_delete=models.CASCADE)
#     relative_name = models.CharField(max_length=255)
#     relationship = models.CharField(max_length=255)

# class Videos(models.Model):
#     star = models.ForeignKey(Star, on_delete=models.CASCADE)
#     video_url = models.URLField()

# class OtherWorks(models.Model):
#     star = models.ForeignKey(Star, on_delete=models.CASCADE)
#     work_description = models.TextField()

class StarType (models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
      return self.name

class Star(models.Model): 
    name = models.CharField(max_length=100) 
    # star_type = models.ForeignKey(StarType, on_delete=models.CASCADE)
    job = models.ManyToManyField(StarType, related_name='stars', blank=True)
    history = models.TextField(blank=True,null=False)
    height = models.FloatField(null=False, blank=True,default=0,help_text="height in meters.")
    born_date = models.DateField(null=True, blank=True)
    born_location = models.CharField(null=True, blank=True,max_length=255)
    died_date = models.DateField(null=True, blank=True)
    died_location = models.CharField(null=True, blank=True,max_length=255)
    update_time = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class Official_sites(models.Model):
    star = models.ForeignKey(Star, on_delete=models.CASCADE)
    name_site = models.CharField(null=False,max_length=100) 
    Official_sites = models.URLField(null=False,max_length=2000)

    def __str__(self):
        return f"I for {self.star.name}"

# class StarImage(models.Model):
#     star = models.ForeignKey(Star, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='stars/')
#     mainimage = models.BooleanField(default=False, verbose_name="Is Main")
#     active = models.BooleanField(default=True, verbose_name="Is Active")
    
#     def __str__(self):
#         return f"Image for {self.star.name}"

# class StarImageURL(models.Model):
#     star = models.ForeignKey(Star, on_delete=models.CASCADE)
#     image_url = models.URLField(max_length=2000)
#     active = models.BooleanField(default=True, verbose_name="Is Active")

#     def __str__(self):
#         return f"Image for {self.star.name}"

class AlternativeNames(models.Model):
    star = models.ForeignKey(Star, on_delete=models.CASCADE)
    alternative_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.alternative_name

class Spouses(models.Model):
    star = models.ForeignKey(Star, on_delete=models.CASCADE)
    spouse = models.ForeignKey(Star, on_delete=models.SET_NULL, null=True, related_name='spouse_star')
    marriage_date = models.DateField()
    divorce = models.BooleanField(default=False)
    divorce_date = models.DateField(null=True, blank=True)

class Children(models.Model):
    star = models.ForeignKey(Star, on_delete=models.CASCADE)
    child_name = models.ForeignKey(Star, on_delete=models.SET_NULL, null=True, related_name='children_star')

    def __str__(self):
        return self.star.name

class Relatives(models.Model):
    star = models.ForeignKey(Star, on_delete=models.CASCADE)
    relative_name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=255)

class OtherWorks(models.Model):
    star = models.ForeignKey(Star, on_delete=models.CASCADE)
    work_description = models.TextField()