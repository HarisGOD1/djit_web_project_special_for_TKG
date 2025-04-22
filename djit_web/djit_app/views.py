from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def this_may_be_any_name(request):
    return HttpResponse("Hello world!")

def this_etc(request):
    template = loader.get_template('greet.html')
    return HttpResponse(template.render({'user' : request.user},request))

def main_page(request):
    template = loader.get_template('mainpage.html')
    return HttpResponse(template.render({'user' : request.user},request))

def guide_first_setup(request):
    template = loader.get_template('guidefirstsetup.html')
    return HttpResponse(template.render({'user' : request.user},request))
