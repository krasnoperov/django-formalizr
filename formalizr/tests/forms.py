from django import forms

from formalizr.tests.models import SimpleModel


class SimpleForm(forms.Form):
    value = forms.IntegerField()


class SimpleModelForm(forms.ModelForm):
    class Meta:
        model = SimpleModel
