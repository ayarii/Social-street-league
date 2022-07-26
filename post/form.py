
from dataclasses import fields
from django import forms
from .models import Post


    
class post_form(forms.ModelForm):
    class Meta:
        model = Post 
        fields = ('post_title','post_description','post_date' ,'post_location','post_image' ,)
        widgets= {
            'post_title':forms.TextInput(attrs={'class':'form-control'}),
            'post_description': forms.Textarea(attrs={'class':'form-control'}),
            'post_date':forms.DateTimeInput(attrs={'class': 'form-control ' }),
            'post_location': forms.TextInput(attrs={'class':'form-control'}),
            'post_image': forms.FileInput(attrs={'class':'form-control'}),
        }
      