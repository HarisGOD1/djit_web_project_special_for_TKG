# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import HttpResponse
from django.template import loader

from . import ACLManagerClient
from .forms import SSHKeyForm, RepoCreateForm
from .models import Repository, DjitUser


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required(login_url='/auth/login/')
def profile_information(request):
    template = loader.get_template('registration/profile.html')
    user = request.user
    # djituser_ = user.djituser


    reps = user.djituser.repositories.all()
    print(reps)

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
        user.djituser.isSSHSetup=True
        user.djituser.save()
        response = ACLManagerClient.send(f'setup_ssh_for_user:{user.username}:{sshkey_val}')
        return HttpResponse(f"Hello, {user.username}.\n{response}")

    else:
        form = SSHKeyForm()
        context = {
            'sshkeyform': form
        }


    return HttpResponse(template.render(context,request))


@login_required(login_url='/auth/login/')
def create_repository(request):
    template = loader.get_template('registration/repocreate.html')
    user = request.user
    context = {
        'repocreateform' : None,
    }
    # TO-DO move these logics to service file
    if request.method == 'POST':
        reponame = request.POST['reponame']
        description = request.POST['description']
        visibility = request.POST['visibility']
        isprivate = True if visibility=='private' else False

        # print(user.djituser.objects.all())
        fl = user.djituser.isSSHSetup
        print(fl)
        problem = 'ssh isnt setup'
        for e in user.djituser.repositories.all():
            if e.repository_name == reponame:
                problem = 'repo yet existed'
                fl = False

        if fl:
            repo = Repository.objects.create(repository_name=reponame,
                                             repository_description=description,
                                             repository_privacy=isprivate,
                                             owner_name=user.username,
                                             members_name=[user.username])
            repo.save()
            user.djituser.repositories.add(repo)
            user.djituser.save()
            response = ACLManagerClient.send(f'create_u_repository:{user.username}:{reponame}')

            return HttpResponse(f"Hello, {user.username}.\n{response}")
        else:
            return HttpResponse(f"Hello, {user.username}.\n {problem}!"
                                f"\n <a href=\"/auth/sshkey_add_edit\">here you can setup ssh</a>"
                                f"\n <a href=\"/auth/profile\">here you can see your repositories</a>")

    else:
        form = RepoCreateForm()
        context = {
            'repocreateform': form
        }


    return HttpResponse(template.render(context,request))




