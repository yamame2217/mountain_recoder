from django import forms
from .models import ClimbRecord

class ClimbRecordForm(forms.ModelForm):
    class Meta:
        model = ClimbRecord
        fields = ['climb_date', 'comment']
        widgets = {
            'climb_date': forms.DateInput(attrs={'type': 'date'}),
        }