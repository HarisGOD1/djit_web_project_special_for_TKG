from django.urls import path

from . import views


urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"), #to-do make username rules (exlude @,+,-,_,.)
    path('profile/',views.profile_information,name='name_for_profile_page'),

]