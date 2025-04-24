# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import HttpResponse
from django.template import loader

from .terminalAPI import sshkey_manager
from .terminalAPI import repository_manager
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

        response = sshkey_manager.save_ssh(user.username,sshkey_val)
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
            response = repository_manager.create_user_repository(user.username,reponame)

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

# @login_required(login_url='/auth/login/')
def show_repository(request):
    template = loader.get_template('registration/repo_contents.html')
    
    # Get parameters from request
    username = request.GET.get('u')
    repo_name = request.GET.get('r')
    path = request.GET.get('p', '')  # Default to root if no path provided
    
    # TODO: Add code to fetch repository contents
    # This is where you'll need to implement the logic to get files and directories
    # The contents should be a list of dictionaries with:
    # - type: 'file' or 'directory'
    # - path: full path of the item
    # - name: display name of the item
    lst = repository_manager.get_content_from_path(username,repo_name,path)
    contents = [
        # Example structure:
        # {'type': 'directory', 'path': 'src', 'name': 'src'},
        # {'type': 'file', 'path': 'README.md', 'name': 'README.md'},
    ]
    print(lst)
    for e in lst:
        contents.append({'type':'directory' if e[0]=='tree' else 'file',
                         'path':path+'/'+e[1],
                         'name':e[1]})
    # Split path into parts for breadcrumb navigation
    print(contents)
    path_parts = []
    if path:
        current_path = ''
        for part in path.split('/'):
            current_path = f"{current_path}/{part}" if current_path else part
            path_parts.append({
                'name': part,
                'path': current_path
            })
    
    context = {
        'username': username,
        'repo_name': repo_name,
        'path_parts': path_parts,
        'contents': contents
    }
    
    return HttpResponse(template.render(context, request))

