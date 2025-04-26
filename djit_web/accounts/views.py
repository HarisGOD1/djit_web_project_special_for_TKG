# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import HttpResponse, JsonResponse
from django.template import loader

from .terminalAPI import sshkey_manager
from .terminalAPI import repository_manager
from .forms import SSHKeyForm, RepoCreateForm
from .models import Repository, DjitUser
from .terminalAPI.repository_manager import get_content_from_path, get_file_from_path


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required(login_url='/auth/login/')
def profile_information(request):
    template = loader.get_template('registration/profile.html')
    user = request.user
    # djituser_ = user.djituser
    userprofile = user


    try:
        profiles_username = request.GET['u']
        userprofile = User.objects.get(username=profiles_username)
    except KeyError:
        pass

    reps = userprofile.djituser.repositories.all()
    # print(reps)
    context = {
        'userprofile': userprofile,
        'user' : user,
        'repositories':reps
    }

    return HttpResponse(template.render(context,request))

@login_required(login_url='/auth/login/')
def add_or_edit_ssh_key(request):
    template = loader.get_template('registration/ssh_setup.html')
    user = request.user
    context = {
        'user' : user,
        'sshkeyform' : None,
    }
    if request.method == 'POST':
        sshkey_val = request.POST['sshkey']
        user.djituser.isSSHSetup=True
        user.djituser.save()

        response = sshkey_manager.save_ssh(user.username,sshkey_val)
        if response == 'ssh add/edit success':
            return redirect('/auth/success?s=ssh')
        else:
            return redirect('/auth/content_unaviable')

    else:
        try:
            must = True if request.GET['t'] == 'm' else False
        except KeyError:
            must = False
        form = SSHKeyForm()
        context = {
            'user' : user,
            'sshkeyform': form,
            'must' : must
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

            return redirect(f'/auth/repo?u={user.username}&r={reponame}&p=')#HttpResponse(f"Hello, {user.username}.\n{response}")
        else:
            if problem == 'repo yet existed':
                return redirect(f'/auth/repo?u={user.username}&r={reponame}&p=')

            return HttpResponse(f"Hello, {user.username}.\n {problem}!"
                                f"\n <a href=\"/auth/sshkey_add_edit\">here you can setup ssh</a>"
                                f"\n <a href=\"/auth/profile\">here you can see your repositories</a>")

    else:
        if request.user.djituser.isSSHSetup:

            form = RepoCreateForm()
            context = {
                'repocreateform': form
            }
        else:
            return redirect('/auth/sshkey_add_edit?t=m')


    return HttpResponse(template.render(context,request))

@login_required(login_url='/auth/login/')
def show_repository(request):
    template = loader.get_template('registration/repo_contents.html')
    
    # Get parameters from request
    username = request.GET.get('u')
    repo_name = request.GET.get('r')
    path = request.GET.get('p', '')  # Default to root if no path provided
    
    # Get repository contents
    # print('repo exist output ' + str(repository_manager.is_repo_exists(username,repo_name)))
    lst = get_content_from_path(username, repo_name, path)

    if lst:
        contents = []
        for e in lst:
            contents.append({
                'type': 'directory' if e[0] == 'tree' else 'file',
                'path': path + '/' + e[1] if path else e[1],
                'name': e[1]
            })

        path_parts = []
        if path:
            current_path = ''
            for part in path.split('/'):
                current_path = f"{current_path}/{part}" if current_path else part
                path_parts.append({
                    'name': part,
                    'path': current_path
                })
        urequest = request.user
        rep_obj = User.objects.get(username=username).djituser.repositories.get(repository_name=repo_name)

        if(rep_obj.repository_privacy==False or username in rep_obj.members_name or urequest.name==username):

            context = {
                'username': username,
                'repo_name': repo_name,
                'path_parts': path_parts,
                'contents': contents
            }

            return HttpResponse(template.render(context, request))
        else:
            return redirect('/auth/content_unaviable')
    else:
        if repository_manager.is_repo_exists(username,repo_name):
            context = {
                'username': username,
                'repo_name': repo_name,
                # 'path_parts': path_parts,
                'contents': 'empty'
            }
            return HttpResponse(template.render(context, request))
        else:
            return redirect('/auth/content_unaviable')


@login_required(login_url='/auth/login/')
def get_repository_contents(request):
    # Get parameters from request
    username = request.GET.get('u')
    repo_name = request.GET.get('r')
    path = request.GET.get('p', '')  # Default to root if no path provided
    
    # Get repository contents
    lst = get_content_from_path(username, repo_name, path)
    contents = []
    for e in lst:
        contents.append({
            'type': 'directory' if e[0] == 'tree' else 'file',
            'path': path + '/' + e[1] if path else e[1],
            'name': e[1]
        })
    
    return JsonResponse(contents, safe=False)

@login_required(login_url='/auth/login/')
def show_file(request):
    template = loader.get_template('registration/fileshow.html')

    # Get parameters from request
    username = request.GET.get('u')
    repo_name = request.GET.get('r')
    path = request.GET.get('p', '')

    # Get file content
    file_content = get_file_from_path(username, repo_name, path)

    # Get file name from path
    file_name = path.split('/')[-1] if path else ''

    # urequest = request.user
    # rep_obj = User.objects.get(username=username).djituser.repositories.get(repository_name=repo_name)
    # print(rep_obj,urequest)

    context = {
        'user': request.user,
        'username': username,
        'repo_name': repo_name,
        'file_name': file_name,
        'file_content': file_content,
        'path': path
    }



    return HttpResponse(template.render(context, request))

def successForward(request):
    template = loader.get_template('registration/anything_success.html')
    success = 'nothing'
    try:
        success = request.GET.get('s')
    except KeyError:
        pass

    context = {
        'user':request.user,
        'success' : success
    }

    return HttpResponse(template.render(context, request))

def contentUnaviable(request):
    template = loader.get_template('registration/content_unaviable.html')
    return HttpResponse(template.render({'user': request.user}, request))
