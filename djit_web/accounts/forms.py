# forms.py
from django import forms

class SSHKeyForm(forms.Form):
    sshkey = forms.CharField(max_length=4200)

class RepoCreateForm(forms.Form):
    reponame = forms.CharField(max_length=256)
    description = forms.CharField(max_length=511)

# class RepoDeleteForm(forms.Form):
#     reponame = forms.CharField(max_length=256)

# class RepoAddMemberForm(forms.Form):
#     reponame = forms.CharField(max_length=256)
#     membername = forms.CharField(max_length=29)




