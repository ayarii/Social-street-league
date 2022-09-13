from cProfile import label
from dataclasses import fields
from tabnanny import verbose
from django import forms
from .models import Post


    
class post_form(forms.ModelForm):
    class Meta:
        model = Post 
        fields = ['post_title','post_description','post_date' ,'post_image','lat','long','tags']
        widgets= {
            'post_title':forms.TextInput(attrs={'class':'form-control'}),
            'post_description': forms.Textarea(attrs={'class':'form-control', "rows":4 ,}),
            'post_date':forms.DateTimeInput(attrs={'class': 'form-control ' ,'type': 'datetime-local'}),
            'post_image': forms.FileInput(attrs={'class':'form-control'}),
            'post_location': forms.TextInput(attrs={'class':'form-control','style':'display:none;','title':'Your website'}),
            'lat':forms.TextInput(attrs={'class':'form-control','id':'lat', 'size':'12','style':'display:none;'}),
            'long': forms.TextInput(attrs={'class':'form-control','id':'long', 'size':'12','style':'display:none;'}),
            'tags' :forms.Textarea(attrs={'class':'form-control'}),
        }
      