from exceptions import LivreIndisponibleError, QuotaEmpruntDepasseError, MembreInexistantError, LivreInexistantError
from datetime import datetime
import pandas as pd
import csv 
class Livre:
    def __init__(self,isbn,titre,auteur,annee,genre,statut="disponible"): 
        self.isbn=isbn
        self.titre=titre
        self.auteur=auteur
        self.annee=annee
        self.genre=genre
        self.statut=statut
    
    def __str__(self):
        return f"le livre {self.titre} écrit par {self.auteur} en {self.annee} est {self.statut}"

class Membre:
    def __init__(self,id_membre,nom,):
        self.id_membre=id_membre
        self.nom=nom
        self.livres_emprunts=[]
  
    def emprunter(self,livre : Livre ):
        if livre.statut=="disponible":
            self.livres_emprunts.append(livre)
            livre.statut="emprunté"
        else :
            raise LivreIndisponibleError(f"Le livre '{livre.titre}' est emprunté par quelqu'un d'autre.")
    
    def retourner(self,livre : Livre):
        if livre in self.livres_emprunts:
            self.livres_emprunts.remove(livre)
            livre.statut="disponible"
        else :
            raise QuotaEmpruntDepasseError(f"Le livre '{livre.titre}' n'a été emprunté par {self.nom}.")
        
class Bibliotheque:
    def __init__(self):
        self.livres=[]
        self.membres=[]
        self.historique=[]
    def ajouter_livre(self,livre):
        self.livres.append(livre)
    def supprimer_livre(self,livre):
        self.livres.remove(livre)			
    def ajouter_membre(self,membre):
        self.membres.append(membre)
    
    def emprunter_livre(self, id_membre, titre_livre):
        membre = None
        for i in self.membres:
            if i.id_membre == id_membre:
                membre = i
        livre = None
        for i in self.livres:
            if i.titre == titre_livre:
                livre = i
        if not membre:
            raise MembreInexistantError("Membre introuvable")
        elif not livre:
            raise LivreInexistantError("Livre introuvable")
        else:
            membre.emprunter(livre)
            self.historique.append( (datetime.now().strftime("%Y-%m-%d"), id_membre, titre_livre, "emprunt") )

    def retourner_livre(self, id_membre, titre_livre):
        membre = None
        for i in self.membres:
            if i.id_membre == id_membre:
                membre = i
        livre = None
        for i in self.livres:
            if i.titre == titre_livre:
                livre = i
        if not membre:
            raise MembreInexistantError("Membre introuvable")
        elif not livre:
            raise LivreInexistantError("Livre introuvable")
        else:
            membre.retourner(livre)
            self.historique.append( (datetime.now().strftime("%Y-%m-%d"), id_membre, titre_livre, "retour") )
    #les fontions de statistiques
    def genre_livres(self):
        genre_compts={}
        genres = [livre.genre for livre in self.livres]
        if not genres:
            return{}
        for genre in genres:
            if genre in genre_compts:
                genre_compts[genre]+=1
            else:
                genre_compts[genre]=1
        return genre_compts
    
    def top_10_auteurs(self):
        auteurs=[livre.auteur for membre in self.membres for livre in membre.livres_emprunts]
        if not auteurs:
            return {}
        
        df =pd.Series(auteurs)
        top_10 = df.value_counts().head(10)
        return list(top_10.items())

    def emprunts_dernier_30j(self):
        data = self.historique
        
        dates = [datetime.strptime(d, "%Y-%m-%d").date() for d, _, _, a in data if a == "emprunt"]
        if not dates:
            return {}

        df = pd.Series(dates)
        compt = df.value_counts().sort_index()
        seuil_date = (pd.Timestamp.now() - pd.Timedelta(days=30)).date()
        compt_30j = compt[compt.index > seuil_date]

        return {dt.strftime("%Y-%m-%d"): int(nb) for dt, nb in compt_30j.items()}
    #fonction de chargement et sauvgardes des données
    def charger_livres(self):
        try:
            with open("data/livres.txt", "r", encoding="utf-8") as f:
                for line in f:
                    isbn, titre, auteur, annee, genre, statut = line.strip().split(";")
                    self.livres.append(Livre(isbn, titre, auteur, int(annee), genre, statut))
        except FileNotFoundError:
            self.livres = []
    
    def charger_membres(self):
        try:
            with open("data/membres.txt", "r", encoding="utf-8") as f:
                for line in f:
                    id, nom, *livres_emprunts_isbn = line.strip().split(";")
                    membre = Membre(id, nom)
                    if livres_emprunts_isbn:
                        for isbn in livres_emprunts_isbn[0].split(","):
                            for livre in self.livres:
                                if livre.isbn==isbn:
                                    membre.livres_emprunts.append(livre)
                                
                    self.membres.append(membre)
        except FileNotFoundError:
            self.membres = []
    
    def charger_historique(self):
        try:
            with open("data/historique.csv", "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)
                self.historique = list(reader)
        except FileNotFoundError:
            self.historique = []

    def sauvegarder_livres(self):
        with open("data/livres.txt", "w", encoding="utf-8") as f:
            for l in self.livres:
                f.write(f"{l.isbn};{l.titre};{l.auteur};{l.annee};{l.genre};{l.statut}\n")

    def sauvegarder_membres(self):
        with open("data/membres.txt", "w", encoding="utf-8") as f:
            for m in self.membres:
                isbns = ",".join(l.isbn for l in m.livres_emprunts)
                f.write(f"{m.id_membre};{m.nom};{isbns}\n")

    def sauvegarder_historique(self):
        with open("data/historique.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "id_membre", "titre_livre", "action"])
            writer.writerows(self.historique)
    
    def charger_donnees(self):
        self.charger_livres()
        self.charger_membres()
        self.charger_historique()

    def sauvegarder_donnees(self):
        self.sauvegarder_livres()
        self.sauvegarder_membres()
        self.sauvegarder_historique()