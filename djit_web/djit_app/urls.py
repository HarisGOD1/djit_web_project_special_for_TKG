from django.urls import path
from . import views

urlpatterns = [
    path('helloworld/', views.this_may_be_any_name, name='helloworldname'),
    path('helloworld2/',views.this_etc, name='hell2'),
]
