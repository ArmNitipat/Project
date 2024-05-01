# from django import forms
# from .models import Star, StarType, Movie

# class MovieAdminForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(MovieAdminForm, self).__init__(*args, **kwargs)
#         writer_type = StarType.objects.get(name="writer")
#         self.fields['writer'].queryset = Star.objects.filter(job=writer_type)

#     class Meta:
#         model = Movie
#         fields = '__all__'

from django import forms
from .models import LocalImage, URLImage

class LocalImageForm(forms.ModelForm):
    class Meta:
        model = LocalImage
        fields = ['image', 'mainstar', 'mainmovie', 'is_visible', 'star', 'movie']

class URLImageForm(forms.ModelForm):
    class Meta:
        model = URLImage
        fields = ['image_url', 'mainstar', 'mainmovie', 'is_visible', 'star', 'movie']
