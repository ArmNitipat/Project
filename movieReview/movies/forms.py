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
