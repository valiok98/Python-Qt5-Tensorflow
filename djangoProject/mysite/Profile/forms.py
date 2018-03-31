from django import forms

from .models import PersonalProfile

class Form(forms.ModelForm):
    class Meta:
        model = PersonalProfile
        fields = [
            "f_name",
            "l_name",
            "nick_name",
            "age"
        ]
