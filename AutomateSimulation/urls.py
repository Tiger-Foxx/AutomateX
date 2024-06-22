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
    path('liste_automate/', liste_automate, name='liste_automate'),
    path('editer_description/<int:automate_id>', editer_description, name='editer_description'),
    path('supprimer/<int:automate_id>', supprimer, name='supprimer'),
    
    path('create_automate_par_description/', create_automate_par_description, name='create_automate_par_description'),
    path('tester/<int:automate_id>/', page_test, name='tester'),
    path('create_automate_from_regex/', create_automate_from_regex, name='create_automate_from_regex'),
    path('automate/<int:automate_id>/creer_determinise/', creer_determinise, name='creer_determinise'),
    path('automate/<int:automate_id>/creer_minimise/', creer_minimise, name='creer_minimise'),
    path('automate/<int:automate_id>/creer_complet/', creer_complet, name='creer_complet'),
    # path('determinise_automate/<int:automate_id>/', views.determinise_automate, name='determinise_automate'),
    # path('minimise_automate/<int:automate_id>/', views.minimise_automate, name='minimise_automate'),
    # path('complementaire_automate/<int:automate_id>/', views.complementaire_automate, name='complementaire_automate'),
    # path('eliminer_epsilon_transitions/<int:automate_id>/', views.eliminer_epsilon_transitions, name='eliminer_epsilon_transitions')
]
