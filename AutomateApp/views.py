from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from AutomateApp.models import *
from .classes.classes import construire_automate_thompson, Automate as AutomateClass,eliminer_epsilon_transitions,Etat as EtatClass,Transition as TransitonClass
# Create your views here.



def index(request):
    return render(request, 'AutomateApp/index.html')

def create_automate_par_description(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        automate = Automate(nom=nom)
        automate.save()
        return redirect('editer_description', automate_id=automate.id)
    return render(request, 'AutomateApp/EntrerNom.html')


def editer_description(request, automate_id):
    automate = get_object_or_404(Automate, id=automate_id)
    if request.method == 'POST':
        if 'etat' in request.POST:
            nom = request.POST.get('nom')
            is_initial = True if request.POST.get('is_initial') else False
            is_final = True if request.POST.get('is_final') else False
            etat = Etat(nom=nom, is_initial=is_initial, is_final=is_final, automate=automate)
            etat.save()
        elif 'transition' in request.POST:
            etat_depart_id = request.POST.get('etat_depart')
            etat_arrivee_id = request.POST.get('etat_arrivee')
            etiquette = request.POST.get('etiquette')
            etat_depart = get_object_or_404(Etat, id=etat_depart_id)
            etat_arrivee = get_object_or_404(Etat, id=etat_arrivee_id)
            transition = Transition(etat_depart=etat_depart, etat_arrivee=etat_arrivee, etiquette=etiquette)
            transition.save()
        return redirect('editer_description', automate_id=automate.id)

    etats = Etat.objects.filter(automate=automate)
    transitions = Transition.objects.filter(etat_depart__automate=automate)
    return render(request, 'AutomateApp/description.html', {'automate': automate, 'etats': etats, 'transitions': transitions})


def create_automate_from_regex(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        regex = request.POST.get('regex')
        not_async = request.POST.get('not async')
        determinist = request.POST.get('determinist')

        # Créer l'automate de Thomson à partir de l'expression régulière
        automate_class = construire_automate_thompson(regex)

        # Éliminer les transitions epsilon si spécifié
        if not_async and not determinist:
            automate_class=eliminer_epsilon_transitions(automate_class)

        # Déterminer l'automate si spécifié
        if determinist:
            # Éliminer les transitions epsilon d'abord si nécessaire
            automate_class=automate_class.eliminer_epsilon_transitions()
            if not automate_class.est_deterministe()[0]:
                print("on va determniniser")   
                automate_class = automate_class.determiniser()
        

        # Convertir l'automate de Thomson en modèle Django et sauvegarder en base de données
        automate_django = Automate_to_django(automate_class,nom)

        return redirect('index')

    return render(request, 'AutomateApp/expression_reguliere.html')

































































































def Automate_to_django(automate_class, nom):
        """
        Convertit cet objet Automate Python en objet Automate Django et sauvegarde en base de données.
        
        Args:
            nom (str): Le nom de l'automate.
        
        Returns:
            Automate: L'objet Automate Django correspondant.
        """
        automate_django = Automate(nom=nom)
        automate_django.save()

        etats_map = {}
        for etat in automate_class.etats:
            etat_django = Etat(nom=etat.nom, is_initial=etat.is_initial, is_final=etat.is_final, automate=automate_django)
            etat_django.save()
            etats_map[etat.nom] = etat_django

        for transition in automate_class.transitions:
            etat_depart_django = etats_map[transition.etat_depart.nom]
            etat_arrivee_django = etats_map[transition.etat_arrivee.nom]
            transition_django = Transition(etat_depart=etat_depart_django, etat_arrivee=etat_arrivee_django, etiquette=transition.etiquette)
            transition_django.save()

        return automate_django   