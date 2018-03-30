#-*- coding: utf-8 -*-
from django import forms

class DataForm(forms.Form):
   name = forms.CharField(max_length = 100)
   file = forms.FileField(required=False)