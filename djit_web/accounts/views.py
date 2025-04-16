# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import HttpResponse
from django.template import loader


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def profile_information(request):
    template = loader.get_template('registration/profile.html')
    return HttpResponse(template.render())

