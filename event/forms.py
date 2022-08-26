from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields =[
            'title_event',
            'description_event',
            'image',
            'location_event',
            'date_event',
            'Activity_event',
            'Category_event',
            'date',
            'time',
            'created',
        ] 

        widgets =  {
            'title_event': forms.TextInput(attrs={'class':'form-control'}),
            'description_event': forms.Textarea(attrs={'class':'form-control' , "rows":4}),
            'image': forms.FileInput(attrs={'class':'form-control'}),
            'location_event': forms.TextInput(attrs={'class':'form-control'}),
            'date_event': forms.DateTimeInput(attrs={'class':'form-control','type': 'datetime-local'}),
            'Activity_event': forms.Select(attrs={'class':'form-control'}),
            'Category_event': forms.Select(attrs={'class':'form-control'}),
            'date': forms.DateTimeInput(attrs={'class':'form-control' ,'type': 'datetime-local'}),
            'time': forms.DateTimeInput(attrs={'class':'form-control' ,'type': 'datetime-local'}),
            'created': forms.DateTimeInput(attrs={'class':'form-control' ,'type': 'datetime-local'}),




        }