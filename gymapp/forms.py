from django import forms
from .models import Member

class UserDetailForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email', 'phone', 'dob', 'membership']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
