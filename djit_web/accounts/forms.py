# forms.py
from django import forms

class SSHKeyForm(forms.Form):
    sshkey = forms.CharField(max_length=4200)


