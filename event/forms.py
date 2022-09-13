from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields =[
            'title_event',
            'description_event',
            'image',
            'affiche',
            'location_event',
            'date_event',
            'Activity_event',
           
        ] 

        widgets =  {
            'title_event': forms.TextInput(attrs={'class':'form-control'}),
            'description_event': forms.Textarea(attrs={'class':'form-control' , "rows":4}),
            'image': forms.FileInput(attrs={'class':'form-control'}),
            'affiche': forms.FileInput(attrs={'class':'form-control'}),
            'location_event': forms.TextInput(attrs={'class':'form-control'}),
            'date_event': forms.DateTimeInput(attrs={'class':'form-control','type': 'datetime-local'}),
            'Activity_event': forms.Select(attrs={'class':'form-control'}),   
        
        }