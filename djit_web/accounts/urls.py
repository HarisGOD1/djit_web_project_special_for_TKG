from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"), #to-do make username rules (exlude @,+,-,_,.)
    path('profile/',views.profile_information,name='name_for_profile_page'),
    path('sshkey_add_edit/', views.add_or_edit_ssh_key, name='name_for_sshkey_add_edit'),
    path('repository_create/', views.create_repository, name='name_for_repository_create'),
    path('repo/', views.show_repository, name='show_repository'),
    path('repo/api/contents/', views.get_repository_contents, name='get_repository_contents'),
    path('showfile/', views.show_file, name='show_file'),
] + static('/accounts/templates/static/')