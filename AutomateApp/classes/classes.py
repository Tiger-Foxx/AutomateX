


compteur_etat = 0
def generer_nom_etat():
    """
    Génère un nom unique pour un état en utilisant un compteur global.
    """
    global compteur_etat
    nom = f"q{compteur_etat}"
    compteur_etat += 1
    return nom
class Etat:
  """
  Cette classe représente un état avec un nom, un booléen indiquant s'il est initial et un autre indiquant s'il est final.

  Attributs:
    nom (str): Le nom de l'état.
    is_initial (bool): True si l'état est initial, False sinon.
    is_final (bool): True si l'état est final, False sinon.

  Méthodes:
    make_initial(): Définit l'état comme initial.
    make_final(): Définit l'état comme final.
    make_non_initial(): Définit l'état comme non initial.
    make_non_final(): Définit l'état comme non final.
  """

  def __init__(self, nom='', is_initial=False, is_final=False):
    """
    Constructeur de la classe `Etat`.

    Args:
      nom (str): Le nom de l'état.
      is_initial (bool, optional): True si l'état est initial, False par défaut.
      is_final (bool, optional): True si l'état est final, False par défaut.
    """
    self.nom = nom if nom else generer_nom_etat()

    self.is_initial = is_initial
    self.is_final = is_final

  def make_initial(self):
    """
    Définit l'état comme initial.
  """
    self.is_initial = True

  def make_final(self):
    """
    Définit l'état comme final.
  """
    self.is_final = True

  def make_non_initial(self):
    """
    Définit l'état comme non initial.
  """
    self.is_initial = False

  def make_non_final(self):
    """
    Définit l'état comme non final.
  """
    self.is_final = False



class EtatDFA:
    """
    Classe intermédiaire représentant un état du DFA durant la conversion.
    
    Attributs:
        nom (str): Nom de l'état, sous forme de chaîne de caractères représentant un ensemble d'états NFA.
        etats_nfa (frozenset): Ensemble des états NFA représentés par cet état DFA.
        is_final (bool): Indique si l'état est final.
    """
    
    def __init__(self, nom, etats_nfa):
        """
        Constructeur de la classe EtatDFA.

        Args:
            nom (str): Nom de l'état, sous forme de chaîne de caractères représentant un ensemble d'états NFA.
            etats_nfa (frozenset): Ensemble des états NFA représentés par cet état DFA.
        """
        self.nom = nom
        self.etats_nfa = etats_nfa
        self.is_final = any(etat.is_final for etat in etats_nfa)

    def __eq__(self, other):
        """
        Vérifie l'égalité entre deux états DFA.
        
        Args:
            other (EtatDFA): L'autre état à comparer.
        
        Returns:
            bool: True si les états sont égaux, False sinon.
        """
        return self.etats_nfa == other.etats_nfa

    def __hash__(self):
        """
        Calcule le hash de l'état DFA pour utilisation dans des ensembles ou des dictionnaires.
        
        Returns:
            int: Le hash de l'état.
        """
        return hash(self.nom)

class Fragment:
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Transition:
  """
  Cette classe représente une transition d'un automate à états finis.

  Attributs:
    etat_depart (Etat): L'état de départ de la transition.
    etat_arrivee (Etat): L'état d'arrivée de la transition.
    etiquette (str): L'étiquette de la transition (peut être la chaîne vide).
    is_epsilon_transition (bool): True si l'étiquette est la chaîne vide, False sinon.

  Méthodes:
    __init__(self, etat_depart, etat_arrivee, etiquette="", is_epsilon_transition=None):
      Constructeur de la transition.
  """

  def __init__(self, etat_depart, etat_arrivee, etiquette="", is_epsilon_transition=None):
    """
    Constructeur de la transition.

    Args:
      etat_depart (Etat): L'état de départ de la transition.
      etat_arrivee (Etat): L'état d'arrivée de la transition.
      etiquette (str, optional): L'étiquette de la transition (défaut: "").
      is_epsilon_transition (bool, optional): True si l'étiquette est la chaîne vide (défaut: None).
    """
    self.etat_depart = etat_depart
    self.etat_arrivee = etat_arrivee
    self.etiquette = etiquette

    if is_epsilon_transition is None:
      self.is_epsilon_transition = etiquette == ""
    else:
      self.is_epsilon_transition = is_epsilon_transition

  def __str__(self):
    """
    Renvoie une représentation textuelle de la transition.

    Returns:
      str: La représentation textuelle de la transition.
    """
    if self.is_epsilon_transition:
      return f"({self.etat_depart.nom}, ε, {self.etat_arrivee.nom})"
    else:
      return f"({self.etat_depart.nom}, {self.etiquette}, {self.etat_arrivee.nom})"



class Automate:
  """
  Cette classe représente un automate à états finis.

  Attributs:
    nom (str): Le nom de l'automate.
    etats (list[Etat]): La liste des états de l'automate.
    transitions (list[Transition]): La liste des transitions de l'automate.
    etats_initiaux (list[Etat]): La liste des états initiaux de l'automate.
    etats_finaux (list[Etat]): La liste des états finaux de l'automate.
    is_determinist (bool): True si l'automate est déterministe, False sinon.

  Méthodes:
    __init__(self, nom, etats=None, transitions=None):
      Constructeur de l'automate.
    add_etat(self, etat): Ajoute un état à l'automate.
    add_transition(self, transition): Ajoute une transition à l'automate.
    etats_initiaux(self): Renvoie la liste des états initiaux.
    etats_finaux(self): Renvoie la liste des états finaux.
    verifier_transition(self, etat_depart, etiquette, etat_arrivee):
      Vérifie si une transition existe entre deux états avec une étiquette donnée.
    est_deterministe(self):
      Vérifie si l'automate est déterministe.
    verifier_mot(self, mot):
      Vérifie si un mot est reconnu par l'automate.
    chemin_reconnu(self, mot):
      Renvoie un chemin possible pour un mot reconnu, ou None si le mot n'est pas reconnu.
  """

  def __init__(self, nom, etats=None, transitions=None):
    """
    Constructeur de l'automate.

    Args:
      nom (str): Le nom de l'automate.
      etats (list[Etat], optional): La liste des états initiaux de l'automate (défaut: []).
      transitions (list[Transition], optional): La liste des transitions initiales de l'automate (défaut: []).
    """
    self.nom = nom
    self.etats = etats or []
    self.transitions = transitions or []
    self.etats_initiaux = [etat for etat in self.etats if etat.is_initial]
    self.etats_finaux = [etat for etat in self.etats if etat.is_final]
    self.is_determinist = self.est_deterministe()[0]

  def add_etat(self, etat):
    """
    Ajoute un état à l'automate.

    Args:
      etat (Etat): L'état à ajouter.
    """
    if etat not in self.etats:
      self.etats.append(etat)
      if etat.is_initial:
        self.etats_initiaux.append(etat)
      if etat.is_final:
        self.etats_finaux.append(etat)
      self.is_determinist = self.est_deterministe()[0]

  def add_transition(self, transition):
    """
    Ajoute une transition à l'automate.

    Args:
      transition (Transition): La transition à ajouter.
    """
    if (transition.etat_depart not in self.etats) or (transition.etat_arrivee not in self.etats):
      raise ValueError("Les états de la transition doivent appartenir à l'automate.")
    self.transitions.append(transition)
    self.is_determinist = self.est_deterministe()[0]

  def etats_initiaux(self):
    """
    Renvoie la liste des états initiaux.

    Returns:
      list[Etat]: La liste des états initiaux.
    """
    return self.etats_initiaux

  def etats_finaux(self):
    """
    Renvoie la liste des états finaux.

    Returns:
      list[Etat]: La liste des états finaux.
    """
    return self.etats_finaux

  def verifier_transition(self, etat_depart, etiquette, etat_arrivee):
      """
      Vérifie si une transition existe entre deux états avec une étiquette donnée.

      Args:
          etat_depart (Etat): L'état de départ.
          etiquette (str): L'étiquette de la transition.
          etat_arrivee (Etat): L'état d'arrivée.

      Returns:
          bool: True si la transition existe, False sinon.
      """

      for transition in self.transitions:
          if (transition.etat_depart == etat_depart) and (transition.etiquette == etiquette) and (transition.etat_arrivee == etat_arrivee):
              return True
      return False
    
  def est_deterministe(self):
        """
        Vérifie si l'automate est déterministe.

        Returns:
            tuple: (booléen, str) indiquant si l'automate est déterministe et une raison si ce n'est pas le cas.
        """
        raisons = []

        # Vérification des états initiaux multiples
        if len(self.etats_initiaux) > 1:
            raisons.append("Plusieurs états initiaux.")

        # Vérification des transitions sortantes multiples avec la même étiquette ou epsilon-transitions
        for etat in self.etats:
            etiquettes = {}
            for transition in self.transitions:
                if transition.etat_depart == etat:
                    if transition.is_epsilon_transition:
                        raisons.append(f"Transition epsilon de l'état {etat.nom}.")
                    elif transition.etiquette in etiquettes:
                        raisons.append(f"Multiples transitions sortantes avec l'étiquette '{transition.etiquette}' de l'état {etat.nom}.")
                    else:
                        etiquettes[transition.etiquette] = transition.etat_arrivee

        return (len(raisons) == 0, "Déterministe" if len(raisons) == 0 else ", ".join(raisons))

  def get_alphabet(self):
          """
          Retourne l'alphabet de l'automate en parcourant ses transitions.

          Returns:
              set: Ensemble des symboles de l'alphabet de l'automate.
          """
          alphabet = {transition.etiquette for transition in self.transitions if transition.etiquette != ""}
          return alphabet
  def est_complet(self):
          """
          Vérifie si l'automate est complet.

          Returns:
              bool: True si l'automate est complet, False sinon.
          """
          for etat in self.etats:
              transitions_sortantes = {t.etiquette for t in self.transitions if t.etat_depart == etat}
              if self.get_alphabet() - transitions_sortantes:
                  return False
          return True

  def contient_transitions_vides(self):
        """
        Vérifie si l'automate contient des transitions epsilon.

        Returns:
            bool: True si des transitions epsilon existent, False sinon.
        """
        return any(transition.etiquette=="" or transition.etiquette=='' for transition in self.transitions)
  def trier_etats(self):
        """
        Trie la liste des états par ordre alphabétique de leur nom.
        """
        self.etats.sort(key=lambda etat: etat.nom)
 
  def determiniser(self):
        """
        Convertit un automate non déterministe (NFA) en un automate déterministe (DFA) en utilisant la méthode de sous-ensemble.
        
        Returns:
            Automate: Le DFA résultant de la conversion.
        """
        etats_dfa = []  # Liste pour stocker les états intermédiaires du DFA
        transitions_dfa = []  # Liste pour stocker les transitions intermédiaires du DFA

        # L'état initial du DFA est l'ensemble des états initiaux du NFA
        etat_initial_nfa = frozenset(self.etats_initiaux)
        etat_initial_dfa = EtatDFA("{%s}" % ",".join(etat.nom for etat in etat_initial_nfa), etat_initial_nfa)
        etats_dfa.append(etat_initial_dfa)
        pile_a_traiter = [etat_initial_dfa]  # Pile des états DFA à traiter

        while pile_a_traiter:
            etat_courant_dfa = pile_a_traiter.pop()  # Récupère un état DFA à traiter

            # Pour chaque symbole de l'alphabet
            for lettre in {t.etiquette for t in self.transitions if t.etiquette}:
                nouveaux_etats = set()  # Ensemble des nouveaux états NFA atteignables
                # Trouver tous les états atteignables par ce symbole
                for etat_nfa in etat_courant_dfa.etats_nfa:
                    for transition in self.transitions:
                        if transition.etat_depart == etat_nfa and transition.etiquette == lettre:
                            nouveaux_etats.add(transition.etat_arrivee)

                if nouveaux_etats:
                    # Créer un nouvel état DFA pour cet ensemble d'états NFA
                    nouveaux_etats_frozenset = frozenset(nouveaux_etats)
                    nom_nouveaux_etats = "{%s}" % ",".join(etat.nom for etat in nouveaux_etats)
                    etat_dfa_existant = next((e for e in etats_dfa if e.etats_nfa == nouveaux_etats_frozenset), None)
                    if not etat_dfa_existant:
                        # Si l'état DFA n'existe pas déjà, le créer
                        nouvel_etat_dfa = EtatDFA(nom_nouveaux_etats, nouveaux_etats_frozenset)
                        etats_dfa.append(nouvel_etat_dfa)
                        pile_a_traiter.append(nouvel_etat_dfa)
                    else:
                        nouvel_etat_dfa = etat_dfa_existant

                    # Ajouter la transition au DFA
                    transitions_dfa.append(Transition(etat_courant_dfa, nouvel_etat_dfa, lettre))

        # Création des états du DFA final en utilisant la classe Etat
        etats_dfa_final = []
        etat_mapping = {}  # Pour mapper les noms d'états DFA intermédiaires aux objets Etat

        for etat_dfa in etats_dfa:
            nouvel_etat = Etat(etat_dfa.nom, is_initial=(etat_dfa == etat_initial_dfa), is_final=etat_dfa.is_final)
            etats_dfa_final.append(nouvel_etat)
            etat_mapping[etat_dfa.nom] = nouvel_etat

        # Création des transitions du DFA final
        transitions_dfa_final = []
        for transition in transitions_dfa:
            transitions_dfa_final.append(
                Transition(etat_mapping[transition.etat_depart.nom], etat_mapping[transition.etat_arrivee.nom], transition.etiquette)
            )

        # Créer le nouveau automate DFA
        automate_dfa = Automate("DFA_" + self.nom)
        automate_dfa.etats = etats_dfa_final
        automate_dfa.transitions = transitions_dfa_final
        automate_dfa.etats_initiaux = [etat for etat in etats_dfa_final if etat.is_initial]
        automate_dfa.etats_finaux = [etat for etat in etats_dfa_final if etat.is_final]

        return automate_dfa


  def get_etat_by_nom(self, nom):
        for etat in self.etats:
            if etat.nom == nom:
                return etat
        return None

  def verifier_mot(self, mot):
        etait_async = False
        
        calcul = []
        if mot == "":
            for etat in self.etats_initiaux:
                if etat.is_final:
                    calcul.append(f"({etat.nom},ε,{etat.nom})-final")
                    return True, 0, " ".join(calcul)
            return False, 0, " ".join(calcul)

        etats_actuels = [etat for etat in self.etats if etat.is_initial]
        for index, lettre in enumerate(mot):
            prochains_etats = []
            for etat in etats_actuels:
                for transition in self.transitions:
                    if transition.etat_depart == etat and transition.etiquette == lettre:
                        prochains_etats.append(transition.etat_arrivee)
                        calcul.append(f"({transition.etat_depart.nom},{lettre},{transition.etat_arrivee.nom})")
            if not prochains_etats:
                calcul="calcul  -----    impossible"
                return False, index, " ".join(calcul)
            etats_actuels = prochains_etats

        is_reconnu = any(etat.is_final for etat in etats_actuels)
        if is_reconnu:
            calcul.append("-final")
        else:
            calcul.append("-non final")
            
        if etait_async:
            calcul=" Nous avons elimites les transitions asynchrones vant le test"
        return is_reconnu, len(mot) if is_reconnu else -1, " ".join(calcul)


  def minimiser(self):
        """
        Minimise l'automate en utilisant l'algorithme de minimisation de Moore.

        Returns:
            Automate: Le nouvel automate minimisé.
        """
        # Si l'automate n'est pas déterministe, le déterminiser d'abord
        if not self.is_determinist:
            print(f"je determinise ")
            self = self.determiniser()
        if not self.est_complet():
            print(f"je cmplete ")
            self=self.completer()
        # print("on demarre avec l'automate : ")
        # afficher_automate(self)
        # Initialisation de la partition initiale
        # P est la partition des états, initialisée avec deux ensembles :
        # - Les états finaux
        # - Les états non finaux
        P = [set(self.etats_finaux), set(self.etats) - set(self.etats_finaux)]
        # W est l'ensemble des ensembles à traiter, initialisé de la même manière que P
        W = [set(self.etats_finaux), set(self.etats) - set(self.etats_finaux)]

        # Boucle principale de l'algorithme
        while W:
            # Prendre un ensemble de W
            A = W.pop()
            # Pour chaque symbole de l'alphabet
            for lettre in {t.etiquette for t in self.transitions if t.etiquette}:
                # X est l'ensemble des états qui ont une transition vers A avec l'étiquette actuelle
                X = {t.etat_depart for t in self.transitions if t.etat_arrivee in A and t.etiquette == lettre}
                for Y in P.copy():
                    # inter est l'intersection de Y et X
                    inter = Y & X
                    # diff est la différence de Y et X
                    diff = Y - X
                    if inter and diff:
                        # Si inter et diff sont non vides, remplacer Y par inter et diff dans P
                        P.remove(Y)
                        P.append(inter)
                        P.append(diff)
                        # Mettre à jour W en conséquence
                        if Y in W:
                            W.remove(Y)
                            W.append(inter)
                            W.append(diff)
                        else:
                            if len(inter) <= len(diff):
                                W.append(inter)
                            else:
                                W.append(diff)

        # Création des nouveaux états et des nouvelles transitions
        etat_map = {}
        for i, subset in enumerate(P):
            # Créer un nouveau nom pour chaque ensemble d'états
            nom = "{" + ",".join(sorted(etat.nom for etat in subset)) + "}"
            # Déterminer si l'état est initial ou final
            is_initial = any(etat.is_initial for etat in subset)
            is_final = any(etat.is_final for etat in subset)
            # Créer un nouvel état et le stocker dans le mapping
            etat_map[frozenset(subset)] = Etat(nom, is_initial, is_final)

        # Liste des nouveaux états
        new_etats = list(etat_map.values())
        # Liste des nouvelles transitions
        new_transitions = []
        for subset in P:
            for lettre in {t.etiquette for t in self.transitions if t.etiquette}:
                etat_source = etat_map[frozenset(subset)]
                for etat in subset:
                    for transition in self.transitions:
                        if transition.etat_depart == etat and transition.etiquette == lettre:
                            etat_cible = next(etat_map[frozenset(sub)] for sub in P if transition.etat_arrivee in sub)
                            new_transitions.append(Transition(etat_source, etat_cible, lettre))
                            break

        # Création du nouvel automate minimisé
        automate_minimise = Automate("Minimisé_" + self.nom)
        automate_minimise.etats = new_etats
        automate_minimise.transitions = new_transitions
        automate_minimise.etats_initiaux = [etat for etat in new_etats if etat.is_initial]
        automate_minimise.etats_finaux = [etat for etat in new_etats if etat.is_final]

        return automate_minimise
  def completer(self):
    """
    Complète un automate non déterministe en ajoutant un état puits pour les transitions manquantes.

    Args:
        automate (Automate): L'automate à compléter.

    Returns:
        Automate: L'automate complété.
    """
    # Déterminer l'alphabet en parcourant les transitions
    alphabet = set()
    for transition in self.transitions:
        if transition.etiquette:
            alphabet.add(transition.etiquette)

    # Créer un état puits
    etat_puit = Etat("puit")
    self.add_etat(etat_puit)
    # Ajouter des transitions vers l'état puits pour les transitions manquantes
    for etat in self.etats:
        for lettre in alphabet:
            if not any(t.etiquette == lettre and t.etat_depart == etat for t in self.transitions):
                self.add_transition(Transition(etat, etat_puit, lettre))

    # Ajouter les transitions pour l'état puits lui-même
    for lettre in alphabet:
        self.add_transition(Transition(etat_puit, etat_puit, lettre))

    # Ajouter l'état puits à l'automate
    self.add_etat(etat_puit)

    return self

  def complementaire(self):
        """
        Construit l'automate complémentaire.

        Returns:
            Automate: L'automate complémentaire.
        """
        # Étape 1 : Déterminiser l'automate
        if not self.est_deterministe()[0]:
          self = self.determiniser()

        # Étape 2 : Compléter l'automate s'il n'est pas complet
        if not self.est_complet():
            self.completer()

        # Étape 3 : Inverser les états finaux et non finaux
        for etat in self.etats:
            etat.is_final = not etat.is_final

        return self
  def eliminer_epsilon_transitions(self):
        """
        Élimine les transitions epsilon de cet automate.

        Returns:
            AutomateClass: Un nouvel automate sans transitions epsilon.
        """
        new_automate = Automate("SansEpsilon_" + self.nom)

        # Copie des états
        etat_map = {etat: Etat(etat.nom, etat.is_initial, etat.is_final) for etat in self.etats}
        #new_automate.etats = list(etat_map.values())
        for etat in list(etat_map.values()):
            new_automate.add_etat(etat)

        # Collecte des epsilon-closures
        epsilon_closures = {}
        for etat in self.etats:
            closure = set()
            to_visit = [etat]
            while to_visit:
                current = to_visit.pop()
                if current not in closure:
                    closure.add(current)
                    for transition in self.transitions:
                        if transition.etat_depart == current and transition.is_epsilon_transition:
                            to_visit.append(transition.etat_arrivee)
            epsilon_closures[etat] = closure

        # Ajout des transitions sans epsilon
        for transition in self.transitions:
            if not transition.is_epsilon_transition:
                for etat_depart in epsilon_closures[transition.etat_depart]:
                    for etat_arrivee in epsilon_closures[transition.etat_arrivee]:
                        new_automate.add_transition(Transition(etat_map[etat_depart], etat_map[etat_arrivee], transition.etiquette))

        # Mise à jour des états initiaux et finaux
        for etat in self.etats:
            if etat.is_initial:
                for closure_state in epsilon_closures[etat]:
                    etat_map[closure_state].make_initial()
            if etat.is_final:
                for closure_state in epsilon_closures[etat]:
                    etat_map[closure_state].make_final()

        return new_automate
 
      
def eliminer_epsilon_transitions(automate):
    """
    Élimine les transitions epsilon d'un automate.

    Args:
        automate (Automate): L'automate à transformer.

    Returns:
        Automate: Un nouvel automate sans transitions epsilon.
    """
    new_automate = Automate("SansEpsilon_" + automate.nom)

    # Copie des états
    etat_map = {etat: Etat(etat.nom, etat.is_initial, etat.is_final) for etat in automate.etats}
    #new_automate.etats = list(etat_map.values())
    for etat in list(etat_map.values()):
            new_automate.add_etat(etat)

    # Collecte des epsilon-closures
    epsilon_closures = {}
    for etat in automate.etats:
        closure = set()
        to_visit = [etat]
        while to_visit:
            current = to_visit.pop()
            if current not in closure:
                closure.add(current)
                for transition in automate.transitions:
                    if transition.etat_depart == current and transition.is_epsilon_transition:
                        to_visit.append(transition.etat_arrivee)
        epsilon_closures[etat] = closure

    # Ajout des transitions sans epsilon
    for transition in automate.transitions:
        if not transition.is_epsilon_transition:
            for etat_depart in epsilon_closures[transition.etat_depart]:
                for etat_arrivee in epsilon_closures[transition.etat_arrivee]:
                    new_automate.add_transition(Transition(etat_map[etat_depart], etat_map[etat_arrivee], transition.etiquette))

    # Mise à jour des états initiaux et finaux
    for etat in automate.etats:
        if etat.is_initial:
            for closure_state in epsilon_closures[etat]:
                etat_map[closure_state].make_initial()
        if etat.is_final:
            for closure_state in epsilon_closures[etat]:
                etat_map[closure_state].make_final() 

    return new_automate



def automate_mot_vide():
        """
        Construit un automate qui reconnaît uniquement le mot vide.

        Returns:
            Automate: L'automate qui reconnaît uniquement le mot vide.
        """
        # Créer un état initial qui est également un état final
        etat_initial_final = Etat("q0", is_initial=True, is_final=True)

        # Créer l'automate
        automate = Automate("Automate_Mot_Vide")
        automate.add_etat(etat_initial_final)

        return automate
def afficher_automate(automate):
    #automate.trier_etats()
    """
    Affiche les états et transitions d'un automate.

    Args:
        automate (Automate): L'automate à afficher.
    """ 
    print(f"type Etats : {type(automate.etats[0])} type transitions : {type(automate.transitions)}")
    print(f"automate deterministe ? : {automate.is_determinist}")
    print("États")
    for etat in (automate.etats):
        print(f"État: {etat.nom}, Initial: {etat.is_initial}, Final: {etat.is_final}")
    print("\nTransitions")
    for transition in automate.transitions:
        print(f"{transition.etat_depart.nom} --{transition.etiquette}--> {transition.etat_arrivee.nom}")

############################# METHODE DE THOMPSON ########################################
#########################################################################################



def construire_automate_caractere(caractere):
    """
    Construit un automate de Thomson pour un caractère unique.
    
    Args:
        caractere (str): Le caractère unique.

    Returns:
        Automate: L'automate de Thomson correspondant au caractère.
    """
    start = Etat( is_initial=True)
    end = Etat( is_final=True)
    
    transition = Transition(start, end, caractere)
    
    automate = Automate(f"A_{caractere}")
    automate.add_etat(start)
    automate.add_etat(end)
    automate.add_transition(transition)
    
    return automate
  
  
  
def construire_etoile_kleene(automate):
    """
    Construit l'étoile de Kleene d'un automate.
    
    Args:
        automate (Automate): L'automate de base.

    Returns:
        Automate: L'automate résultant de l'application de l'étoile de Kleene.
    """
    start = Etat(is_initial=True)
    end = Etat(is_final=True)
    
    new_automate = Automate(f"K_{automate.nom}")
    
    new_automate.add_etat(start)
    new_automate.add_etat(end)
    
    for etat in automate.etats:
        new_automate.add_etat(etat)
        
    for transition in automate.transitions:
        new_automate.add_transition(transition)
    #l'ancien etat initial ne l'est plus
    automate.etats_initiaux[0].make_non_initial()
    # Transition de qs vers l'état initial de l'automate
    new_automate.add_transition(Transition(start, automate.etats_initiaux[0], ""))
    
    # Transition de qs vers qf (pour l'étoile de Kleene vide)
    new_automate.add_transition(Transition(start, end, ""))
    
    # Transition des états finaux de l'automate vers qf et vers l'état initial
    for i,final_state in enumerate(automate.etats_finaux):
        final_state.make_non_final()
        automate.etats_finaux[i].make_non_final()
        new_automate.add_transition(Transition(final_state, end, ""))
        new_automate.add_transition(Transition(final_state, automate.etats_initiaux[0], ""))
        
        

    return new_automate

def construire_concatenation(automate1, automate2):
    """
    Construit l'automate de Thomson pour la concaténation de deux automates.
    
    Args:
        automate1 (Automate): Le premier automate.
        automate2 (Automate): Le deuxième automate.

    Returns:
        Automate: L'automate résultant de la concaténation des deux automates.
    """
    new_automate = Automate(f"C_{automate1.nom}_{automate2.nom}")
    #l'ancien etat initial ne l'est plus
    for i, final_state in enumerate(automate2.etats_initiaux):
        automate2.etats_initiaux[i].make_non_initial()
    automate1.etats_finaux[0].make_non_final()
    for etat in automate1.etats:
        new_automate.add_etat(etat)
        
    for etat in automate2.etats:
        new_automate.add_etat(etat)
    
    for transition in automate1.transitions:
        new_automate.add_transition(transition)
        
    for transition in automate2.transitions:
        new_automate.add_transition(transition)
    
    
    # Transition des états finaux de automate1 vers l'état initial de automate2
    for i, final_state in enumerate(automate1.etats_finaux):
        automate1.etats_finaux[i].make_non_final()
        final_state.make_non_final()
        new_automate.add_transition(Transition(final_state, automate2.etats_initiaux[0], ""))
        
        
    
    
    return new_automate

def construire_union(automate1, automate2):
    """
    Construit l'automate de Thomson pour l'union de deux automates.
    
    Args:
        automate1 (Automate): Le premier automate.
        automate2 (Automate): Le deuxième automate.

    Returns:
        Automate: L'automate résultant de l'union des deux automates.
    """
    start = Etat(is_initial=True)
    end = Etat(is_final=True)
    
    new_automate = Automate(f"U_{automate1.nom}_{automate2.nom}")
    
    new_automate.add_etat(start)
    new_automate.add_etat(end)
    #l'ancien etat initial ne l'est plus
    automate1.etats_initiaux[0].make_non_initial()
    #l'ancien etat initial ne l'est plus
    automate2.etats_initiaux[0].make_non_initial()
    #l'ancien etat initial ne l'est plus
    automate1.etats_finaux[0].make_non_final()
    #l'ancien etat initial ne l'est plus
    automate2.etats_finaux[0].make_non_final()
    for etat in automate1.etats:
        new_automate.add_etat(etat)
        
    for etat in automate2.etats:
        new_automate.add_etat(etat)
    
    for transition in automate1.transitions:
        new_automate.add_transition(transition)
        
    for transition in automate2.transitions:
        new_automate.add_transition(transition)
    
    # Transitions de qs vers les états initiaux de automate1 et automate2
    new_automate.add_transition(Transition(start, automate1.etats_initiaux[0], ""))
    new_automate.add_transition(Transition(start, automate2.etats_initiaux[0], ""))
    
    # Transitions des états finaux de automate1 et automate2 vers qf
    for final_state in automate1.etats_finaux:
        new_automate.add_transition(Transition(final_state, end, ""))
        final_state.make_non_final()
        
    for final_state in automate2.etats_finaux:
        new_automate.add_transition(Transition(final_state, end, ""))
        final_state.make_non_final()
    

    return new_automate


def analyser_expression(expression):
    """
    Analyse une expression régulière pour séparer les caractères et les sous-expressions entre parenthèses.

    Args:
        expression (str): L'expression régulière.

    Returns:
        list: Une liste contenant les caractères et les sous-expressions.
    """
    resultat = []
    pile = []
    sous_expression = ""
    for char in expression:
        if char == '(':
            if pile:
                sous_expression += char
            pile.append(char)
        elif char == ')':
            pile.pop()
            if pile:
                sous_expression += char
            else:
                resultat.append(analyser_expression(sous_expression))
                sous_expression = ""
        else:
            if pile:
                sous_expression += char
            else:
                resultat.append(char)
    return resultat

# Exemple d'utilisation
# expression = "a(b+c)*dkkk(abc+l)"
# analyse = analyser_expression(expression)
# print(analyse)

def creer_automate_aa():
    etat1 = Etat("1", is_initial=True, is_final=False)
    etat2 = Etat("2", is_initial=False, is_final=False)
    etat3 = Etat("3", is_initial=False, is_final=True)

    t1 = Transition(etat1, etat2, "a")
    t2 = Transition(etat2, etat3, "a")
    t3 = Transition(etat1, etat1, "b")
    t4 = Transition(etat2, etat1, "b")
    t5 = Transition(etat3, etat3, "a")
    t6 = Transition(etat3, etat3, "b")

    automate = Automate("Automate_AA")
    automate.add_etat(etat1)
    automate.add_etat(etat2)
    automate.add_etat(etat3)
    automate.add_transition(t1)
    automate.add_transition(t2)
    automate.add_transition(t3)
    automate.add_transition(t4)
    automate.add_transition(t5)
    automate.add_transition(t6)

    return automate



def precedence(op):
    """
    Renvoie la priorité de l'opérateur pour les expressions régulières.
    """
    if op == '*':
        return 3
    if op == '.':
        return 2
    if op == '+':
        return 1
    return 0
  
  
def infix_to_postfix(expression):
    """
    Convertit une expression régulière infixée en notation postfixée (polonaise inversée).

    Args:
        expression (str): L'expression régulière.

    Returns:
        str: L'expression régulière en notation postfixée.
    """
    stack = []
    output = []
    for char in expression:
        if char.isalnum():
            output.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and precedence(stack[-1]) >= precedence(char):
                output.append(stack.pop())
            stack.append(char)
    while stack:
        output.append(stack.pop())
    return ''.join(output)

# # Exemple d'utilisation
# expression = "a+b"
# postfix_expression = infix_to_postfix(expression)
# print(postfix_expression)  # Devrait afficher "ab+"

def ajouter_points(expression):
    """
    Ajoute explicitement des opérateurs de concaténation ('.') dans une expression régulière infixée.

    Args:
        expression (str): L'expression régulière sans opérateurs de concaténation explicites.

    Returns:
        str: L'expression régulière avec des opérateurs de concaténation explicites.
    """
    resultat = ""
    for i in range(len(expression)):
        resultat += expression[i]
        if i + 1 < len(expression):
            if (expression[i].isalnum() or expression[i] == ')' or expression[i] == '*') and \
               (expression[i + 1].isalnum() or expression[i + 1] == '('):
                resultat += '.'
    return resultat

# Exemple d'utilisation
# expression = "a+b"
# expression_avec_points = ajouter_points(expression)
# print(expression_avec_points)  # Devrait afficher "a.+b"



def infix_to_postfix(expression):
    """
    Convertit une expression régulière infixée en notation postfixée (polonaise inversée).

    Args:
        expression (str): L'expression régulière.

    Returns:
        str: L'expression régulière en notation postfixée.
    """
    expression = ajouter_points(expression)
    stack = []
    output = []
    for char in expression:
        if char.isalnum():  # Caractère alphanumérique
            output.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # Retirer la parenthèse ouvrante
        else:
            while stack and precedence(stack[-1]) >= precedence(char):
                output.append(stack.pop())
            stack.append(char)
    while stack:
        output.append(stack.pop())
    return ''.join(output)

# Exemple d'utilisation
# expression = "a(b+c)*d"
# postfix_expression = infix_to_postfix(expression)
# print(postfix_expression)  # Devrait afficher "abc+*.d."

def construire_automate_a_plus_b():
    """
    Construit l'automate de Thomson pour l'expression régulière 'a+b'.
    
    Returns:
        Automate: L'automate de Thomson correspondant à l'expression régulière 'a+b'.
    """
    # Créer l'automate pour le caractère 'a'
    start_a = Etat("q0", is_initial=True)
    end_a = Etat("q1", is_final=True)
    transition_a = Transition(start_a, end_a, "a")

    automate_a = Automate("Automate_a")
    automate_a.add_etat(start_a)
    automate_a.add_etat(end_a)
    automate_a.add_transition(transition_a)

    # Créer l'automate pour le caractère 'b'
    start_b = Etat("q2", is_initial=True)
    end_b = Etat("q3", is_final=True)
    transition_b = Transition(start_b, end_b, "b")

    automate_b = Automate("Automate_b")
    automate_b.add_etat(start_b)
    automate_b.add_etat(end_b)
    automate_b.add_transition(transition_b)

    # Créer l'union des automates 'a' et 'b'
    start_union = Etat("qs", is_initial=True)
    end_union = Etat("qf", is_final=True)

    automate_union = Automate("Automate_a_plus_b")
    automate_union.add_etat(start_union)
    automate_union.add_etat(end_union)

    # Ajouter les états et transitions de 'a'
    for etat in automate_a.etats:
        automate_union.add_etat(etat)
    for transition in automate_a.transitions:
        automate_union.add_transition(transition)

    # Ajouter les états et transitions de 'b'
    for etat in automate_b.etats:
        automate_union.add_etat(etat)
    for transition in automate_b.transitions:
        automate_union.add_transition(transition)

    # Ajouter les transitions pour l'union
    automate_union.add_transition(Transition(start_union, start_a, ""))
    automate_union.add_transition(Transition(start_union, start_b, ""))
    automate_union.add_transition(Transition(end_a, end_union, ""))
    automate_union.add_transition(Transition(end_b, end_union, ""))

    # Marquer les états finaux des sous-automates comme non finaux
    end_a.make_non_final()
    end_b.make_non_final()

    return automate_union

def construire_automate_thompson(expression):
    postfix_expression=infix_to_postfix(expression)
    print(postfix_expression)
    if postfix_expression=="":
        return automate_mot_vide()
    stack = []
    for char in postfix_expression:
        if char.isalnum():
            stack.append(construire_automate_caractere(char))
        elif char == '*':
            nfa = stack.pop()
            stack.append(construire_etoile_kleene(nfa))
        elif char == '+':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(construire_union(nfa1, nfa2))
        elif char == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(construire_concatenation(nfa1, nfa2))
    if len(stack) != 1:
        raise ValueError("Expression régulière invalide")
    global compteur_etat
    compteur_etat=0
    
    return stack.pop()

# Exemple d'utilisation
# expression = "a+b"
# nfa = construire_automate_thompson(expression)
# afficher_automate(nfa.eliminer_epsilon_transitions().minimiser())
# print("on  enfin l'automate : ")
# afficher_automate(construire_automate_a_plus_b().eliminer_epsilon_transitions().minimiser())


########################### TESTS ##########################################
############################################################################


def test_automate(automate, mot):
    reconnu, index , calcul= automate.verifier_mot(mot)
    if reconnu:
        print(f"Le mot '{mot}' est reconnu par l'automate.")
    else:
        if index == -1:
            print(f"Le mot '{mot}' n'est pas reconnu par l'automate.")
        else:
            print(f"Le mot '{mot[:index]}' est lu mais pas sa suite '{mot[index:]}' votre mot n'est pas reconniu par l'automate.")
 

def tester_mot():
    expression = "ab*"
    automate= construire_automate_thompson(expression).eliminer_epsilon_transitions() 
    while True :           
      mot=input("entre le mot : ")
      test_automate(automate,mot)

#tester_mot()


def test_NFA():

  # Exemple d'automate NFA
  etat1 = Etat("1", is_initial=True, is_final=False)
  etat2 = Etat("2", is_initial=False, is_final=False)
  etat3 = Etat("3", is_initial=False, is_final=True)
  etat4 = Etat("4", is_initial=False, is_final=False)

  # Création des transitions du NFA
  t1 = Transition(etat1, etat1, "a")
  t2 = Transition(etat1, etat2, "a")
  t3 = Transition(etat1, etat4, "b")
  t4 = Transition(etat2, etat3, "b")
  t5 = Transition(etat3, etat3, "a")
  t6 = Transition(etat3, etat3, "b")
  t7 = Transition(etat4, etat3, "a")

  # Création de l'automate NFA
  automate_nfa = Automate("NFA")
  automate_nfa.add_etat(etat1)
  automate_nfa.add_etat(etat2)
  automate_nfa.add_etat(etat3)
  automate_nfa.add_etat(etat4)
  automate_nfa.add_transition(t1)
  automate_nfa.add_transition(t2)
  automate_nfa.add_transition(t3)
  automate_nfa.add_transition(t4)
  automate_nfa.add_transition(t5)
  automate_nfa.add_transition(t6)
  automate_nfa.add_transition(t7)

  # Conversion en DFA
  automate_dfa = automate_nfa.determiniser()

  # Affichage des états et des transitions du DFA
  print("États du DFA:")
  for etat in automate_dfa.etats:
      print(f"État: {etat.nom}, Initial: {etat.is_initial}, Final: {etat.is_final}")

  print("\nTransitions du DFA:")
  for transition in automate_dfa.transitions:
      print(f"{transition.etat_depart.nom} --{transition.etiquette}--> {transition.etat_arrivee.nom}")



def test_determinisation():
    """
    Teste la fonction de déterminisation d'un automate en créant un NFA, le déterminisant et affichant les résultats.
    """
    # Création d'un automate NFA exemple
    etat1 = Etat("1", is_initial=True, is_final=False)
    etat2 = Etat("2", is_initial=False, is_final=False)
    etat3 = Etat("3", is_initial=False, is_final=True)
    etat4 = Etat("4", is_initial=False, is_final=False)

    # Création des transitions du NFA
    t1 = Transition(etat1, etat1, "a")
    t2 = Transition(etat1, etat2, "a")
    t3 = Transition(etat1, etat4, "b")
    t4 = Transition(etat2, etat3, "b")
    t5 = Transition(etat3, etat3, "a")
    t6 = Transition(etat3, etat3, "b")
    t7 = Transition(etat4, etat3, "a")

    # Création de l'automate NFA
    automate_nfa = Automate("NFA")
    automate_nfa.add_etat(etat1)
    automate_nfa.add_etat(etat2)
    automate_nfa.add_etat(etat3)
    automate_nfa.add_etat(etat4)
    automate_nfa.add_transition(t1)
    automate_nfa.add_transition(t2)
    automate_nfa.add_transition(t3)
    automate_nfa.add_transition(t4)
    automate_nfa.add_transition(t5)
    automate_nfa.add_transition(t6)
    automate_nfa.add_transition(t7)

    # Affichage des états et des transitions du NFA
    print("États du NFA:")
    for etat in automate_nfa.etats:
        print(f"État: {etat.nom}, Initial: {etat.is_initial}, Final: {etat.is_final}")

    print("\nTransitions du NFA:")
    for transition in automate_nfa.transitions:
        print(f"{transition.etat_depart.nom} --{transition.etiquette}--> {transition.etat_arrivee.nom}")

    # Conversion en DFA
    automate_dfa = automate_nfa.determiniser()

    # Affichage des états et des transitions du DFA
    print("\nÉtats du DFA:")
    for etat in automate_dfa.etats:
        print(f"État: {etat.nom}, Initial: {etat.is_initial}, Final: {etat.is_final}")

    print("\nTransitions du DFA:")
    for transition in automate_dfa.transitions:
        print(f"{transition.etat_depart.nom} --{transition.etiquette}--> {transition.etat_arrivee.nom}")

# Exécuter le test de déterminisation
#test_determinisation()

def tester_minimisation():
    """
    Teste l'algorithme de minimisation d'un automate.

    Cette fonction crée un automate, applique l'algorithme de minimisation, et vérifie les propriétés de l'automate minimisé.
    """
    # Créer un automate initial avec des états et transitions redondants
    etat1 = Etat("1", is_initial=True, is_final=False)
    etat2 = Etat("2", is_initial=False, is_final=False)
    etat3 = Etat("3", is_initial=False, is_final=True)
    etat4 = Etat("4", is_initial=False, is_final=True)

    transition1 = Transition(etat1, etat2, "a")
    transition2 = Transition(etat2, etat3, "b")
    transition3 = Transition(etat2, etat4, "b")
    transition4 = Transition(etat1, etat1, "a")
    transition5 = Transition(etat1, etat2, "b")
    transition6 = Transition(etat3, etat3, "a")
    transition7 = Transition(etat4, etat4, "a")

    automate_initial = Automate("Automate_Test")
    automate_initial.add_etat(etat1)
    automate_initial.add_etat(etat2)
    automate_initial.add_etat(etat3)
    automate_initial.add_etat(etat4)
    automate_initial.add_transition(transition1)
    automate_initial.add_transition(transition2)
    automate_initial.add_transition(transition3)
    automate_initial.add_transition(transition4)
    automate_initial.add_transition(transition5)
    automate_initial.add_transition(transition6)
    automate_initial.add_transition(transition7)

    print("Automate initial :")
    afficher_automate(automate_initial)

    # Appliquer la minimisation
    automate_minimise = automate_initial.minimiser()

    print("\nAutomate minimisé :")
    afficher_automate(automate_minimise)



# Appeler la fonction de test
#tester_minimisation()


#afficher_automate(creer_automate_aa().complementaire())