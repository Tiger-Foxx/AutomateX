from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from AutomateApp.models import *
from .classes.classes import afficher_automate, construire_automate_thompson, Automate as AutomateClass,eliminer_epsilon_transitions,Etat as EtatClass,Transition as TransitonClass
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

        return redirect('tester',automate_django.id)

    return render(request, 'AutomateApp/expression_reguliere.html')


def liste_automate(request):
    automates = Automate.objects.all()
    automates_info = []

    for automate in automates:
        automate_classe = automate.to_classe()
        automates_info.append({
            'id':automate.id,
            'nom': automate.nom,
            'date_creation': automate.date,
            'nombre_etats': len(automate_classe.etats),
            'is_deterministe': automate_classe.est_deterministe()[0]
        })

    return render(request, 'AutomateApp/liste_automate.html', {'automates_info': automates_info})

def supprimer(request,automate_id):
    
    automate = get_object_or_404(Automate, id=automate_id)
    automate.delete()

    return redirect('liste_automate')



from django.shortcuts import render, get_object_or_404

def page_test(request, automate_id):
    automate = get_object_or_404(Automate, id=automate_id)
    automate_classe = automate.to_classe()
    contient_transitions_vides = automate_classe.contient_transitions_vides()
    if construire_automate_thompson:
        automate_classe=automate_classe.eliminer_epsilon_transitions()
        
    est_complet = automate_classe.est_complet()
    afficher_automate(automate_classe)
    resultat = None
    calcul = "Le calcul s'affiche ici "
    message = "Le Resultat ICI"
    mot = ""
    transitions=automate_classe.transitions
    if request.method == 'POST':
        mot = request.POST.get('mot')
        is_reconnu, position,calcul = automate_classe.verifier_mot(mot)
        if is_reconnu:
            resultat = True
            message = f"Mot reconnu ! "
        else:
            resultat = False
            message = f"Mot non reconnu "

    etats = automate_classe.etats
    etiquettes = list(set(transition.etiquette for transition in automate_classe.transitions ))
    liste_vrai_etats=[]
    i=0
    tableau = []
    if automate_classe.est_deterministe()[0]:
        for etat in etats:
            transitions_list = ["/"] * len(etiquettes)
            for transition in automate_classe.transitions:
                if transition.etat_depart.nom == etat.nom:
                    index = etiquettes.index(transition.etiquette)
                    transitions_list[index] = transition.etat_arrivee.nom
            if etat.is_initial:
                liste_vrai_etats.append(">>"+etat.nom)
            elif etat.is_final:
                liste_vrai_etats.append(etat.nom+">>")
            else :
                liste_vrai_etats.append(etat.nom)
            tableau.append((liste_vrai_etats[i], transitions_list))
            i+=1
        
        
        

        
        for i in range(len(etiquettes)):
            if etiquettes[i] == "" or not etiquettes[i]:
                
                etiquettes[i] = "ε"
    
        
    print(etiquettes)    
    return render(request, 'AutomateApp/detail.html', context={
        'automate': automate,
        'tableau': tableau,
        'etiquettes': etiquettes,
        'resultat': resultat,
        'message': message,
        'calcul': calcul,
        'mot': mot,
        'automate_classe': automate_classe,
        'contient_transitions_vides': contient_transitions_vides,
        'est_complet': est_complet,
        'reconnu':is_reconnu if request.method == 'POST' else None,
        'transitions':transitions,
        'etats':etats,
    })




def creer_determinise(request, automate_id):
    automateModel = get_object_or_404(Automate, id=automate_id)
    
    automate=automateModel.to_classe()
    automate = automate.determiniser()
    nom="determinise_"+automateModel.nom
    A=Automate_to_django(nom=nom,automate_class=automate)
    return redirect('tester', automate_id=A.id)

def creer_minimise(request, automate_id):
    automateModel = get_object_or_404(Automate, id=automate_id)
    automate=automateModel.to_classe()
    automate = automate.minimiser()
    nom="minimise_"+automateModel.nom
    A=Automate_to_django(nom=nom,automate_class=automate)
    return redirect('tester', automate_id=A.id)

def creer_complet(request, automate_id):
    automateModel = get_object_or_404(Automate, id=automate_id)
    automate=automateModel.to_classe()
    automate = automate.completer()
    nom="complet_"+automateModel.nom
    A=Automate_to_django(nom=nom,automate_class=automate)
    return redirect('tester', automate_id=A.id)





















































































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