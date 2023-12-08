from blog.category.models import Category
from django import forms
from django.utils.text import slugify
from unidecode import unidecode

class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        
    
        