from bibliotheque import Livre, Membre, Bibliotheque
import matplotlib.pyplot as plt
#Interface en Ligne de Commande 
def menu():
    print("---Gestion Bibliothèque---")
    print("1. Ajouter un livre")
    print("2. Inscrire un membre")
    print("3. Emprunter un livre")
    print("4. Retourner un livre")
    print("5. Lister tous les livres")
    print("6. Afficher les statistiques")
    print("7. Sauvegarder et Quitter")
    choix =input("choisissez une option (1-7) :")
    #validation de l'entrée
    while choix not in ['1', '2', '3', '4', '5', '6', '7']:
        choix =input("Choix invalide, résssayez (1-7)")
    
    return int(choix)

def main():
    biblio = Bibliotheque()
    biblio.charger_donnees()
    while True:
        choix = menu()
        match choix:
            case  1:
                isbn = input("ISBN du livre : ")
                titre = input("Titre : ")
                auteur = input("Auteur : ")
                annee = input("Année : ")
                genre = input("Genre : ")
                livre = Livre(isbn, titre, auteur, int(annee), genre)
                biblio.ajouter_livre(livre)
                print("Livre ajouté.")

            case 2:
                id_membre = input("ID membre : ")
                nom = input("Nom : ")
                membre = Membre(id_membre, nom)
                biblio.ajouter_membre(membre)
                print("Membre ajouté.")

            case 3:
                id_membre = input("ID membre : ")
                titre = input("Titre du livre à emprunter : ")
                try:
                    biblio.emprunter_livre(id_membre, titre)
                    print("Livre emprunté avec succès.")
                except Exception as e:
                    print("Erreur :", e)

            case 4:
                id_membre = input("ID membre : ")
                titre = input("Titre du livre à retourner : ")
                try:
                    biblio.retourner_livre(id_membre, titre)
                    print("Livre retourné avec succès.")
                except Exception as e:
                    print("Erreur :", e)

            case 5:
                print("La liste des livres :")
                for livre in biblio.livres:
                    print(livre)
            
            case 6:
                print("Les statistiques :")
                print("Pourcentage des livres par genre :")
                genre_compts=biblio.genre_livres()
                if not genre_compts:
                    print("Aucun livre trouvé")
                labels = list(genre_compts.keys())
                sizes = list(genre_compts.values())
                fig, ax = plt.subplots()
                ax.pie(sizes, labels=labels, autopct='%1.1f%%')
                ax.set_title("Pourcentage des livres par genre")
                plt.show()
                print("les top 10 auteurs :")
                top_10 = biblio.top_10_auteurs()
                if not top_10:
                    print("Aucun emprunt trouvé")
                else:
                    noms=top_10.index.tolist()
                    nbr = top_10.values.tolist()
                
                    fig, ax = plt.subplots()
                    ax.bar(noms, nbr)
                    plt.xlabel("Nom Auteur")
                    plt.ylabel("Nombre d'emprunts")
                    ax.set_xticklabels(noms, rotation=45, ha="right")
                    ax.set_title("Top 10 des auteurs les plus populaires")
                    plt.tight_layout()
                    plt.show()

                print("les emprunts des 30 dérniers jours :")
                compt_30j = biblio.emprunts_dernier_30j()

                if not compt_30j:
                    print("Aucun emprunt trouvé")
                else :
                    x = list(compt_30j.keys())
                    y = list(compt_30j.values())
                    plt.plot(x,y,marker='o', title="Emprunts sur les 30 derniers jours")
                    plt.xlabel("Date")
                    plt.ylabel("Nombre d'emprunts")
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    plt.show()

            case 7:
                print("Sauvegarde en cours...")
                biblio.sauvegarder_donnees()
                print("Données sauvegardées")
                break
                


if __name__ == "__main__":
    main()
