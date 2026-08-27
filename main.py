"""Menu interactif du mini modèle de langage N-grammes."""
import modele as m


def afficher_menu():
    print("\n=========================================")
    print("        MINI MODELE DE LANGAGE")
    print("=========================================")
    print(" 1. Afficher le vocabulaire")
    print(" 2. Afficher les unigrammes")
    print(" 3. Afficher les bigrammes")
    print(" 4. Afficher les trigrammes")
    print(" 5. Calculer une probabilite")
    print(" 6. Predire le mot suivant")
    print(" 7. Generer une phrase")
    print(" 8. Calculer la probabilite d'une phrase")
    print(" 9. Corriger une phrase")
    print("10. Comparer deux phrases")
    print("11. Quitter")
    print("=========================================")


def main():
    while True:
        afficher_menu()
        choix = input("Votre choix : ").strip()

        if choix == "1":
            print("Vocabulaire :", sorted(m.VOCAB))
            print("Taille :", len(m.VOCAB))

        elif choix == "2":
            for mot, freq in m.UNI.most_common():
                print(f"  {mot} : {freq}")

        elif choix == "3":
            for bg, freq in m.BI.most_common():
                print(f"  {bg} : {freq}")

        elif choix == "4":
            for tg, freq in m.TRI.most_common():
                print(f"  {tg} : {freq}")

        elif choix == "5":
            prec = input("  Mot precedent : ").strip().lower()
            mot = input("  Mot : ").strip().lower()
            print(f"  P({mot} | {prec}) = {m.probabilite_bigramme(prec, mot):.4f}")
            print(f"  P Laplace = {m.probabilite_laplace(prec, mot):.4f}")

        elif choix == "6":
            ctx = input("  Contexte : ").strip()
            candidats = m.predire_mot_suivant(ctx)
            if candidats:
                for mot, p in candidats.items():
                    print(f"  {mot} : {p:.4f}")
            else:
                print("  Aucun candidat.")

        elif choix == "7":
            print("  ", " ".join(m.generer_phrase()))

        elif choix == "8":
            ph = input("  Phrase : ").strip()
            print(f"  P = {m.probabilite_phrase(ph):.6f}")
            print(f"  P (Laplace) = {m.probabilite_phrase(ph, laplace=True):.6f}")

        elif choix == "9":
            meilleur, scores = m.corriger_phrase("Il a cet ans")
            print("  Scores :", scores)
            print("  Mot propose :", meilleur)

        elif choix == "10":
            s1 = input("  Phrase 1 : ").strip()
            s2 = input("  Phrase 2 : ").strip()
            p1 = m.probabilite_phrase(s1, laplace=True)
            p2 = m.probabilite_phrase(s2, laplace=True)
            print(f"  P(S1) = {p1:.6f}")
            print(f"  P(S2) = {p2:.6f}")
            print("  Plus probable :", s1 if p1 >= p2 else s2)

        elif choix == "11":
            print("Au revoir !")
            break

        else:
            print("Choix invalide, reessayez.")


if __name__ == "__main__":
    main()
