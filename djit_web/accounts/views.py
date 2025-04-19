# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import HttpResponse
from django.template import loader


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

