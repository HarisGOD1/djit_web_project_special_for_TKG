from django.urls import path
from . import views

urlpatterns = [
    path('helloworld/', views.this_may_be_any_name, name='helloworldname'),
    path('helloworld2/',views.this_etc, name='helloworldname2'),
    path('',views.main_page,name='mainpage_name'),
    path('guide/first-setup',views.guide_first_setup,name='name_for_guide_for_first_setup'),

]
