"""
URL configuration for AutomateSimulation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path
from AutomateApp.views import *
from AutomateSimulation import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    # path('create_transition/', views.create_transition, name='create_transition'),
    path('editer_description/<int:automate_id>', editer_description, name='editer_description'),
    path('create_automate_par_description/', create_automate_par_description, name='create_automate_par_description'),
    # path('edit_automate/<int:automate_id>/', views.edit_automate, name='edit_automate'),
    path('create_automate_from_regex/', create_automate_from_regex, name='create_automate_from_regex'),
    # path('determinise_automate/<int:automate_id>/', views.determinise_automate, name='determinise_automate'),
    # path('minimise_automate/<int:automate_id>/', views.minimise_automate, name='minimise_automate'),
    # path('complementaire_automate/<int:automate_id>/', views.complementaire_automate, name='complementaire_automate'),
    # path('eliminer_epsilon_transitions/<int:automate_id>/', views.eliminer_epsilon_transitions, name='eliminer_epsilon_transitions')
]
