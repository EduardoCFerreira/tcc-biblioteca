from django import forms
from bibliotech.models import Category
from utils.django_forms import add_attr

class CategoriaEditar(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Category
        fields = 'name',