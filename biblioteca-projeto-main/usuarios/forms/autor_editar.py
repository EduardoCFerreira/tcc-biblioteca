from django import forms
from bibliotech.models import Author
from utils.django_forms import add_attr

class AuthorEditar(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Author
        fields = 'name',