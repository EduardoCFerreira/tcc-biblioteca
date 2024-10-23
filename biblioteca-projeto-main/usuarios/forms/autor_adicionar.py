from django import forms
from bibliotech.models import Author
from utils.django_forms import add_attr
from django.core.exceptions import ValidationError
from collections import defaultdict

class AuthorCreate(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

    class Meta:
        model = Author
        fields = 'name',

        def clean(self, *args, **kwargs):
            super_clean = super().clean(*args, **kwargs)
            cleaned_data = self.cleaned_data
            name = cleaned_data.get('name')

            if len(name) > 0:
                self._my_errors['name'].append('O nome da categoria não pode ficar em branco!')

                if self._my_errors:
                    raise ValidationError(self._my_errors)
                
            return super_clean
            
        def clean_name(self):
            name = self.cleaned_data.get('name')
            if len(name) > 0:
                self._my_errors['name'].append('O nome da categoria não pode ficar em branco!')
            return name