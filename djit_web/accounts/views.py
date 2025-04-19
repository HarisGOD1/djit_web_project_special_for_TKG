# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import HttpResponse
from django.template import loader

from . import ACLManagerClient
from .forms import SSHKeyForm


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required(login_url='/auth/login/')
def profile_information(request):
    template = loader.get_template('registration/profile.html')
    user = request.user
    reps = user.djituser.repositories.all()

    context = {
        'user' : user,
        'repositories':reps
    }

    return HttpResponse(template.render(context,request))

@login_required(login_url='/auth/login/')
def add_or_edit_ssh_key(request):
    template = loader.get_template('registration/ssh_setup.html')
    user = request.user
    context = {
        'sshkeyform' : None
    }
    if request.method == 'POST':
        sshkey_val = request.POST['sshkey']
        print(user.username)
        print(sshkey_val)
        response = ACLManagerClient.send(f'setup_ssh_for_user:{user.username}:{sshkey_val}')
        return HttpResponse(f"Hello, {user.username}.\n{response}")

    else:
        form = SSHKeyForm()
        context = {
            'sshkeyform': form
        }


    return HttpResponse(template.render(context,request))



