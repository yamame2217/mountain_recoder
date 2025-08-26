from django import forms
from .models import ClimbRecord, Mountain

class ClimbRecordForm(forms.ModelForm):
    class Meta:
        model = ClimbRecord
        fields = ['climb_date', 'comment', 'image'] 
        widgets = {
            'climb_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MountainForm(forms.ModelForm):
    class Meta:
        model = Mountain
        fields = ['name', 'prefecture', 'elevation']