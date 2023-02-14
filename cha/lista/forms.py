from django import forms

from django import forms
 
# import GeeksModel from models.py
from .models import Product
 
# create a ModelForm
class ProductForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Product
        fields = ['guest_name', 'guest_email']

# class ConvidadoForm(forms.Form):
#     nome = forms.CharField(label='seu nome', max_length=100)
#     email = forms.CharField(label='seu nome', max_length=100)