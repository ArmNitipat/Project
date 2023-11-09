from django.core.exceptions import ValidationError
from django.db import models
from star.models import Star

# Create your models here.


# <------------ Movies ------------>

class MovieTag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class MovieRate(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=100, verbose_name='Movie Name')
    writer = models.ManyToManyField(Star, related_name="written_movies")
    director = models.ManyToManyField(Star, related_name="director_movies")
    release_date = models.DateField(verbose_name='Movie Release Date')
    rate = models.ForeignKey(MovieRate, on_delete=models.SET_NULL, null=True)
    story = models.TextField()
    time = models.CharField(max_length=10, verbose_name='Movie Time')
    tags = models.ManyToManyField(MovieTag, blank=True)
    is_show = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class MovieDetail(models.Model):
    star = models.ForeignKey(Star, on_delete=models.CASCADE)
    is_top = models.BooleanField(default=False, verbose_name='Is Top Star')
    character_name = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.character_name} in {self.movie.name}"


def validate_not_gif(value):
    if value.name.endswith('.gif'):
        raise ValidationError("GIFs are not allowed.")
    return value

class ImageBase(models.Model):
    # Define only the common fields here
    mainstar = models.BooleanField(default=False, null=False)
    mainmovie = models.BooleanField(default=False, null=False)
    is_visible = models.BooleanField(default=True, null=True)

    class Meta:
        abstract = True

class LocalImage(ImageBase):
    image = models.ImageField(upload_to='images/', verbose_name="Image File", validators=[validate_not_gif])
    star = models.ManyToManyField(Star,blank=True, related_name="local_star_images")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True ,blank=True, related_name="local_images_movie")
    
    def __str__(self):
        stars = ', '.join(star.name for star in self.star.all())
        return f"Local Image for Star: {stars} in {self.movie}"        
    # def __str__(self):
    #     return f"Local Image for Star: {self.star.name}"

class URLImage(ImageBase):
    image_url = models.URLField(verbose_name="Image URL")
    star = models.ManyToManyField(Star, blank=True, related_name="url_star_images")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True ,blank=True, related_name="url_movie_images")

    def __str__(self):
        stars = ', '.join(star.name for star in self.star.all())
        return f"Local Image for Star: {stars} in {self.movie}"
    # def __str__(self):
        # return f"URL Image for Star: {self.star.name}"
 

class Video(models.Model):
    title = models.CharField(max_length=200, verbose_name="Video Title")
    video_url = models.URLField(verbose_name="Video URL")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_videos')

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"

    def __str__(self):
        return self.title