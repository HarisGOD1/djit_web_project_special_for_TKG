from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"), #to-do make username rules (exlude @,+,-,_,.)
    path('profile/',views.profile_information,name='name_for_profile_page'),
    path('sshkey_add_edit/', views.add_or_edit_ssh_key, name='name_for_sshkey_add_edit'),
    path('repository_create/', views.create_repository, name='name_for_repository_create'),
    path('repo/', views.show_repository, name='name_for_show_repository'),
    path('repo/api/contents/', views.get_repository_contents, name='name_for_get_repository_contents'),
    path('showfile/', views.show_file, name='name_for_show_file'),
    path('content_unaviable/',views.contentUnaviable,name='name_for_content_unaviable'),
    path('success/',views.successForward, name='name_for_success'),
    path('public/',views.show_public_repositories,name='name_for_show_public_repositories')
] + static('/accounts/templates/static/')