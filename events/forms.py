from django import forms
from events.models import *

class HumanForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not 'class' in field.widget.attrs:
                field.widget.attrs['class'] = "form-control"

    class Meta:
        model = Human
        fields = "__all__"
        labels = {
            "name": "Name",
            "isChild": "Child under 12",
            "email": "Email",
            }
        widgets = {
            "isChild": forms.CheckboxInput(attrs={"class": "form-check-input"})
        }