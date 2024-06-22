from django.db import models
from classes import Etat as EtatClass , Transition as TransitionClass,Automate as AutomateClass 
class Automate(models.Model):
    nom = models.CharField(max_length=100)

    def to_classe(self):
        """
        Convertit cet objet Automate Django en objet Automate Python.
        
        Returns:
            Automate: L'objet Automate Python correspondant.
        """
        automate = AutomateClass(nom=self.nom)
        etats_django = self.etats.all()
        for etat_django in etats_django:
            etat = etat_django.to_classe()
            automate.add_etat(etat)
        
        transitions_django = Transition.objects.filter(etat_depart__automate=self)
        for transition_django in transitions_django:
            transition = transition_django.to_classe()
            automate.add_transition(transition)
        
        return automate

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

class Transition(models.Model):
    etat_depart = models.ForeignKey(Etat, related_name='transitions_depart', on_delete=models.CASCADE)
    etat_arrivee = models.ForeignKey(Etat, related_name='transitions_arrivee', on_delete=models.CASCADE)
    etiquette = models.CharField(max_length=100, blank=True)
    is_epsilon_transition = models.BooleanField(default=False)

    def to_classe(self):
        """
        Convertit cet objet Transition Django en objet Transition Python.
        
        Returns:
            Transition: L'objet Transition Python correspondant.
        """
        etat_depart = self.etat_depart.to_classe()
        etat_arrivee = self.etat_arrivee.to_classe()
        return TransitionClass(etat_depart=etat_depart, etat_arrivee=etat_arrivee, etiquette=self.etiquette, is_epsilon_transition=self.is_epsilon_transition)
