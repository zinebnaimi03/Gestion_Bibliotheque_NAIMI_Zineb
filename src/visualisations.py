import  tkinter as tk
from tkinter import ttk, messagebox
from bibliotheque import Livre, Membre, Bibliotheque
from exceptions import LivreIndisponibleError, QuotaEmpruntDepasseError, LivreInexistantError, MembreInexistantError
import matplotlib.pyplot as plt
from tkinter import Toplevel
from datetime import datetime, timedelta
import pandas as pd
#Instance de la bibliotheque
bib = Bibliotheque()

#Fonction pour ajouter un livre via l'interface
def ajouter_livre():
    #recuperer les valeurs saisies par l'utilisateur
    isbn = entry_isbn.get().strip()
    titre = entry_titre.get().strip()
    auteur = entry_auteur.get().strip()
    annee = entry_annee.get().strip()
    genre = entry_genre.get().strip()
    #verifier que les champs sont valides
    if not (isbn and titre and auteur and annee.isdigit() and genre):
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs correctement.")
        return 
    #creer une instance livre
    livre = Livre(isbn, titre, auteur, int(annee), genre)
    bib.ajouter_livre(livre)
    #ajouter dans le tableau treeview
    tableau_livres.insert('', 'end', values=(isbn, titre, auteur, annee, genre, livre.statut))
    messagebox.showinfo("Succès", f"Livre '{titre}' ajouté.")

    #vider les champs
    entry_isbn.delete(0, tk.END)
    entry_titre.delete(0, tk.END)
    entry_auteur.delete(0, tk.END)
    entry_annee.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
#Fonction pour ajouter un membre via l'interface
def ajouter_membre():
    id_membre = entry_id_membre.get().strip()
    nom = entry_nom.get().strip()

    if not (id_membre and nom):
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
        return 
    membre = Membre(id_membre,nom)
    bib.ajouter_membre(membre)
    tableau_membres.insert('','end', values=(id_membre, nom))
    messagebox.showinfo("Succès", f"Membre '{nom}' ajouté.")
    entry_id_membre.delete(0, tk.END)
    entry_nom.delete(0, tk.END)

#Fonction pour emprunter un livre
def emprunter_livre():
    id_membre = entry_id_membre_emprunter.get().strip()
    titre_livre = entry_titre_emprunter.get().strip()

    try: 
        bib.emprunter_livre(id_membre, titre_livre)
        messagebox.showinfo("Succès", f"Le livre '{titre_livre}' a été emprunté par le membre {id_membre}.")
        actualiser_tableau_emprunts()
        entry_id_membre_emprunter.delete(0, tk.END)
        entry_titre_emprunter.delete(0, tk.END)
    except(LivreIndisponibleError, LivreInexistantError, MembreInexistantError) as e:
        messagebox.showerror("Erreur", str(e))

#Fonction pour retourner un livre
def retourner_livre():
    id_membre = entry_id_membre_retourner.get().strip()
    titre_livre = entry_titre_retourner.get().strip()

    try: 
        bib.retourner_livre(id_membre, titre_livre)
        messagebox.showinfo("Succès", f"Le livre '{titre_livre}' a été retourné par le membre {id_membre}.")
        actualiser_tableau_emprunts()
        entry_id_membre_retourner.delete(0, tk.END)
        entry_titre_retourner.delete(0, tk.END)
    except(QuotaEmpruntDepasseError, LivreInexistantError, MembreInexistantError) as e:
        messagebox.showerror("Erreur", str(e))

#Fonctions pour actualiser les tableaux
def actualiser_tableau_emprunts():
    #vider le tableau pour éviter les doublons 
    for row in tableau_emprunts.get_children():
        tableau_emprunts.delete(row)
    for membre in bib.membres:
        for livre in membre.livres_emprunts:
            tableau_emprunts.insert('', 'end', values=(membre.id_membre, membre.nom, livre.titre))
def actualiser_tableau_livres():
    tableau_livres.delete(*tableau_livres.get_children())
    for livre in bib.livres:
        tableau_livres.insert('', 'end', values=(livre.isbn, livre.titre, livre.auteur, livre.annee, livre.genre, livre.statut))
def actualiser_tableau_membres():
    tableau_membres.delete(*tableau_membres.get_children())
    for membre in bib.membres:
        tableau_membres.insert('', 'end', values=(membre.id_membre, membre.nom))

#Fonctions des statistiques
def afficher_livres_genre():
    genre_compts=bib.genre_livres()
    if not genre_compts:
        messagebox.showinfo("info","Aucun livre trouvé")
        return
    labels = list(genre_compts.keys())
    sizes = list(genre_compts.values())
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax.set_title("Pourcentage des livres par genre")
    plt.savefig("assets/stats_genres.png")
    plt.show()
def afficher_auteurs_livres_empruntes():
    top_10 = bib.top_10_auteurs()
    if not top_10:
        messagebox.showinfo("info", "aucun emprunt trouvé")
        return
    noms = [nom for nom, _ in top_10]
    nbr = [nb for _, nb in top_10]
    fig, ax = plt.subplots()
    ax.bar(noms, nbr)
    ax.set_xlabel("Nom de l’auteur")
    ax.set_ylabel("Nombre d'emprunts")
    ax.set_title("Top 10 des auteurs les plus populaires")
    ax.set_xticks(range(len(noms)))
    ax.set_xticklabels(noms, rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("assets/stats_auteurs.png")
    plt.show()

def afficher_statut_emprunts():
    compt_30j = bib.emprunts_dernier_30j()

    if not compt_30j:
        messagebox.showinfo("info", "Aucun emprunt trouvé")
        return
    x = sorted(compt_30j.keys())
    y = [compt_30j[date] for date in x]
    plt.plot(x, y, marker='o')
    plt.title("Emprunts sur les 30 derniers jours")
   
    plt.xlabel("Date")
    plt.ylabel("Nombre d'emprunts")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("assets/stats_emrpunts.png")
    plt.show()
def sauvegarder_et_afficher():
    bib.sauvegarder_donnees()
    messagebox.showinfo("Sauvegarde", "Les données ont été sauvegardées avec succès.")

def charger_et_afficher():
    bib.charger_donnees()
    messagebox.showinfo("Chargement", "Les données ont été chargées avec succès.")
    actualiser_tableau_livres()
    actualiser_tableau_membres()
    actualiser_tableau_emprunts()
#Création fenêtre principale
root = tk.Tk()
root.title("Gestion Bibliothèque")
root.geometry("900x600")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

#--------------------------tab Livres---------------------
frame_livres = ttk.Frame(notebook)
notebook.add(frame_livres, text="Livres")

ttk.Label(frame_livres, text="ISBN").grid(row=0, column=0, padx=5, pady=5)
entry_isbn = ttk.Entry(frame_livres)
entry_isbn.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_livres, text="titre").grid(row=1, column=0, padx=5, pady=5)
entry_titre = ttk.Entry(frame_livres)
entry_titre.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_livres, text="auteur").grid(row=2, column=0, padx=5, pady=5)
entry_auteur = ttk.Entry(frame_livres)
entry_auteur.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame_livres, text="annee").grid(row=3, column=0, padx=5, pady=5)
entry_annee = ttk.Entry(frame_livres)
entry_annee.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(frame_livres, text="genre").grid(row=4, column=0, padx=5, pady=5)
entry_genre = ttk.Entry(frame_livres)
entry_genre.grid(row=4, column=1, padx=5, pady=5)

btn_ajouter_livre = ttk.Button(frame_livres, text="Ajouter livre", command=ajouter_livre)
btn_ajouter_livre.grid(row=5, column=0, columnspan=2, pady=10)

colonnes_livres = ("ISBN", "Titre", " Auteur", "Année", "Genre", "Statut")
tableau_livres = ttk.Treeview(frame_livres, columns=colonnes_livres, show='headings')
for col in colonnes_livres:
    tableau_livres.heading(col, text=col)
    tableau_livres.column(col, width=100)

tableau_livres.grid(row=6, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

frame_livres.rowconfigure(6, weight=1)
frame_livres.columnconfigure(1, weight=1)
#--------------------------tab Membres---------------------
frame_membres = ttk.Frame(notebook)
notebook.add(frame_membres, text="Membres")

ttk.Label(frame_membres, text="ID Membre").grid(row=0, column=0, padx=5, pady=5)
entry_id_membre = ttk.Entry(frame_membres)
entry_id_membre.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_membres, text="Nom").grid(row=1, column=0, padx=5, pady=5)
entry_nom = ttk.Entry(frame_membres)
entry_nom.grid(row=1, column=1, padx=5, pady=5)


btn_ajouter_membre = ttk.Button(frame_membres, text="Ajouter membre", command=ajouter_membre)
btn_ajouter_membre.grid(row=2, column=0, columnspan=2, pady=10)

colonnes_membres = ("ID", "Nom")
tableau_membres = ttk.Treeview(frame_membres, columns=colonnes_membres, show='headings')
for col in colonnes_membres:
    tableau_membres.heading(col, text=col)
    tableau_membres.column(col, width=100)
    
tableau_membres.grid(row=6, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

frame_membres.rowconfigure(6, weight=1)
frame_membres.columnconfigure(1, weight=1)
#--------------------------tab Emprunts---------------------
frame_emprunts = ttk.Frame(notebook)
notebook.add(frame_emprunts, text="Emprunts")

ttk.Label(frame_emprunts, text="ID Membre").grid(row=0, column=0, padx=5, pady=5)
entry_id_membre_emprunter = ttk.Entry(frame_emprunts)
entry_id_membre_emprunter.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_emprunts, text="Titre Livre").grid(row=1, column=0, padx=5, pady=5)
entry_titre_emprunter = ttk.Entry(frame_emprunts)
entry_titre_emprunter.grid(row=1, column=1, padx=5, pady=5)


btn_emprunter= ttk.Button(frame_emprunts, text="Emprunter", command=emprunter_livre)
btn_emprunter.grid(row=2, column=0, columnspan=2, pady=10)

ttk.Label(frame_emprunts, text="ID Membre").grid(row=3, column=0, padx=5, pady=5)
entry_id_membre_retourner = ttk.Entry(frame_emprunts)
entry_id_membre_retourner.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(frame_emprunts, text="Titre Livre").grid(row=4, column=0, padx=5, pady=5)
entry_titre_retourner = ttk.Entry(frame_emprunts)
entry_titre_retourner.grid(row=4, column=1, padx=5, pady=5)


btn_retourner= ttk.Button(frame_emprunts, text="Retourner", command=retourner_livre)
btn_retourner.grid(row=5, column=0, columnspan=2, pady=10)


colonnes_emprunts = ("ID Membre", "Nom Membre","Titre Livre")
tableau_emprunts = ttk.Treeview(frame_emprunts, columns=colonnes_emprunts, show='headings')
for col in colonnes_emprunts:
    tableau_emprunts.heading(col, text=col)
    tableau_emprunts.column(col, width=150)

tableau_emprunts.grid(row=6, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

frame_emprunts.rowconfigure(6, weight=1)
frame_emprunts.columnconfigure(1, weight=1)

#--------------------------tab Statistiques---------------------
frame_stats = ttk.Frame(notebook)
notebook.add(frame_stats, text="Statistiques")

ttk.Button(frame_stats, text="Par Genre", command=afficher_livres_genre).pack(pady=10)
ttk.Button(frame_stats, text="Top Auteurs", command=afficher_auteurs_livres_empruntes).pack(pady=10)
ttk.Button(frame_stats, text="Emprunts 30 jours", command=afficher_statut_emprunts).pack(pady=10)
ttk.Button(frame_stats, text="Sauvegarder les données", command=lambda: sauvegarder_et_afficher()).pack(pady=5)
ttk.Button(frame_stats, text="Charger les données", command=lambda: charger_et_afficher()).pack(pady=5)
# Application de style
style = ttk.Style()
style.theme_use('clam')  
style.configure('TButton', font=('Helvetica', 10), padding=6, background='#4CAF50', foreground='white')
style.configure('TLabel', font=('Arial', 10, 'bold'))
style.configure('TEntry', padding=5)

style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
style.map('Treeview', background=[('selected', '#4CAF50')])
style = ttk.Style()
style.theme_use('clam')

style = ttk.Style()
style.theme_use('clam')

# Couleur de fond principale
root.configure(bg="#f5f1e6")

# Labels
style.configure("TLabel",
    background="#f5f1e6",
    foreground="#3e2f1c",
    font=("Georgia", 11, "bold")
)

# Entries
style.configure("TEntry",
    background="#fffdf8",
    foreground="#3e2f1c",
    padding=4,
    font=("Georgia", 10),
    relief="flat"
)

# Buttons
style.configure("TButton",
    background="#6b4f29",
    foreground="white",
    font=("Georgia", 10, "bold"),
    padding=6,
    borderwidth=0
)
style.map("TButton",
    background=[("active", "#8c6a3b")]
)

# Treeview (tableaux)
style.configure("Treeview",
    background="#fffdf8",
    foreground="#3e2f1c",
    fieldbackground="#fffdf8",
    rowheight=25,
    font=("Georgia", 10)
)
style.configure("Treeview.Heading",
    font=("Georgia", 11, "bold"),
    background="#bfae94",
    foreground="#3e2f1c"
)
style.map("Treeview",
    background=[("selected", "#e0d3ba")]
)

# Tabs 
style.configure("TNotebook", background="#d6c7ae", borderwidth=0)
style.configure("TNotebook.Tab",
    background="#d6c7ae",
    foreground="#3e2f1c",
    padding=[10, 5],
    font=("Georgia", 10, "bold")
)
style.map("TNotebook.Tab",
    background=[("selected", "#bfae94")],
    foreground=[("selected", "#3e2f1c")]
)

bib.charger_donnees()
actualiser_tableau_livres()
actualiser_tableau_membres()
actualiser_tableau_emprunts()

# lancement de la boucle principale
root.mainloop()