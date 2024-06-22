import datetime
from django.db import models
from .classes.classes import Etat as EtatClass, Transition as TransitionClass, Automate as AutomateClass

class Automate(models.Model):
    nom = models.CharField(max_length=100)
    date=models.DateField(auto_now=True,editable=False)
    def to_classe(self):
        """
        Convertit cet objet Automate Django en objet Automate Python.
        
        Returns:
            AutomateClass: L'objet Automate Python correspondant.
        """
        automate = AutomateClass(nom=self.nom)
        etats_django = self.etats.all()
        etat_map = {}

        for etat_django in etats_django:
            etat = EtatClass(nom=etat_django.nom, is_initial=etat_django.is_initial, is_final=etat_django.is_final)
            automate.add_etat(etat)
            etat_map[etat_django.id] = etat
        
        transitions_django = Transition.objects.filter(etat_depart__automate=self)
        for transition_django in transitions_django:
            etat_depart = etat_map[transition_django.etat_depart.id]
            etat_arrivee = etat_map[transition_django.etat_arrivee.id]
            transition = TransitionClass(etat_depart=etat_depart, etat_arrivee=etat_arrivee, etiquette=transition_django.etiquette, is_epsilon_transition=transition_django.is_epsilon_transition)
            automate.add_transition(transition)
        
        return automate

    def __str__(self):
        return f"Automate {self.nom}" 

class Etat(models.Model):
    nom = models.CharField(max_length=100)
    is_initial = models.BooleanField(default=False)
    is_final = models.BooleanField(default=False)
    automate = models.ForeignKey(Automate, related_name='etats', on_delete=models.CASCADE)

    def to_classe(self):
        """
        Convertit cet objet Etat Django en objet Etat Python.
        
        Returns:
            Etat: L'objet Etat Python correspondant.
        """
        return EtatClass(nom=self.nom, is_initial=self.is_initial, is_final=self.is_final)
    def __str__(self):
        return f"ETAT  {self.nom} | Automate {self.automate.nom}" 

class Transition(models.Model):
    etat_depart = models.ForeignKey(Etat, related_name='transitions_depart', on_delete=models.CASCADE)
    etat_arrivee = models.ForeignKey(Etat, related_name='transitions_arrivee', on_delete=models.CASCADE)
    etiquette = models.CharField(max_length=100, blank=True,default='')
    is_epsilon_transition = models.BooleanField(blank=True , null=True , default=False)

    def to_classe(self):
        """
        Convertit cet objet Transition Django en objet Transition Python.
        
        Returns:
            Transition: L'objet Transition Python correspondant.
        """
        etat_depart = self.etat_depart.to_classe()
        etat_arrivee = self.etat_arrivee.to_classe()
        return TransitionClass(etat_depart=etat_depart, etat_arrivee=etat_arrivee, etiquette=self.etiquette )
    
    def __str__(self):
        return f"TRANSITION DE {self.etat_depart.nom} VERS {self.etat_arrivee.nom} etiquette : {self.etiquette} | Automate {self.etat_arrivee.automate.nom}" 
