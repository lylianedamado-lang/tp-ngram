"""Mini modèle de langage basé sur les N-grammes."""
from collections import Counter

# Le corpus de travail
CORPUS = [
    "Le chat mange du poisson.",
    "Le chat aime le poisson.",
    "Le chien mange de la viande.",
    "Le chien aime la viande.",
    "Le chat joue dans le jardin.",
    "Le chien joue dans le jardin.",
]


def tokeniser(phrase):
    """Transforme une phrase en liste de tokens, avec <s> et </s>."""
    phrase = phrase.lower()                 # 1. tout en minuscules
    for signe in ".,;:!?":                  # 2. on enlève la ponctuation
        phrase = phrase.replace(signe, " ")
    mots = phrase.split()                   # 3. on découpe en mots
    return ["<s>"] + mots + ["</s>"]        # 4. on ajoute les marqueurs


def construire_corpus_tokenise(corpus):
    """Applique la tokenisation à toutes les phrases du corpus."""
    return [tokeniser(p) for p in corpus]


def construire_vocabulaire(corpus_tok):
    """Retourne l'ensemble des mots différents (le vocabulaire)."""
    vocab = set()
    for phrase in corpus_tok:
        for mot in phrase:
            vocab.add(mot)
    return vocab


def construire_unigrammes(corpus_tok):
    """Compte chaque mot (unigramme) dans tout le corpus."""
    freq = Counter()
    for phrase in corpus_tok:
        for mot in phrase:
            freq[mot] += 1
    return freq


def construire_bigrammes(corpus_tok):
    """Compte chaque paire de mots qui se suivent (bigramme)."""
    freq = Counter()
    for phrase in corpus_tok:
        for i in range(len(phrase) - 1):
            freq[(phrase[i], phrase[i+1])] += 1
    return freq


def construire_trigrammes(corpus_tok):
    """Compte chaque suite de 3 mots (trigramme)."""
    freq = Counter()
    for phrase in corpus_tok:
        for i in range(len(phrase) - 2):
            freq[(phrase[i], phrase[i+1], phrase[i+2])] += 1
    return freq


# On calcule les comptages une seule fois, ils serviront partout
CORPUS_TOK = construire_corpus_tokenise(CORPUS)
VOCAB = construire_vocabulaire(CORPUS_TOK)
UNI = construire_unigrammes(CORPUS_TOK)
BI = construire_bigrammes(CORPUS_TOK)
TRI = construire_trigrammes(CORPUS_TOK)


def probabilite_bigramme(mot_precedent, mot):
    """P(mot | mot_precedent) = C(mot_precedent, mot) / C(mot_precedent)."""
    if UNI[mot_precedent] == 0:
        return 0.0
    return BI[(mot_precedent, mot)] / UNI[mot_precedent]



def predire_mot_suivant(contexte):
    """Retourne les mots possibles après le contexte, classés par probabilité."""
    mots = contexte.lower().split()
    dernier = mots[-1] if mots else "<s>"
    candidats = {}
    for (prec, suiv), compte in BI.items():
        if prec == dernier:
            candidats[suiv] = probabilite_bigramme(prec, suiv)
    # on trie du plus probable au moins probable
    return dict(sorted(candidats.items(), key=lambda x: x[1], reverse=True))



def generer_phrase(max_mots=20):
    """Génère une phrase en partant de <s> et en suivant les mots les plus probables."""
    phrase = ["<s>"]
    for _ in range(max_mots):
        candidats = predire_mot_suivant(phrase[-1])
        if not candidats:                 
            break
        suivant = next(iter(candidats))   # le mot le plus probable (1er de la liste triée)
        phrase.append(suivant)
        if suivant == "</s>":            
            break
    return phrase



def probabilite_phrase(phrase, laplace=False):
    """Probabilité d'une phrase = produit des probabilités de ses bigrammes."""
    tokens = tokeniser(phrase)
    p = 1.0
    for i in range(len(tokens) - 1):
        if laplace:
            p *= probabilite_laplace(tokens[i], tokens[i+1])
        else:
            p *= probabilite_bigramme(tokens[i], tokens[i+1])
    return p


# --- Partie 8 : correction contextuelle (corpus supplémentaire) ---
CORPUS2 = [
    "Il a sept ans.",
    "Elle a sept ans.",
    "Mon frere a sept ans.",
    "Il a cet objet.",
    "Elle a cet objet.",
    "Il prend cet objet.",
]
CORPUS2_TOK = construire_corpus_tokenise(CORPUS2)
UNI2 = construire_unigrammes(CORPUS2_TOK)
BI2 = construire_bigrammes(CORPUS2_TOK)


def prob_bigramme_corpus2(mot_precedent, mot):
    """Probabilité bigramme calculée sur le 2e corpus."""
    if UNI2[mot_precedent] == 0:
        return 0.0
    return BI2[(mot_precedent, mot)] / UNI2[mot_precedent]


def corriger_phrase(phrase, candidats=("sept", "cet"), contexte="a"):
    """Compare les candidats après un contexte et propose le plus probable."""
    scores = {c: prob_bigramme_corpus2(contexte, c) for c in candidats}
    meilleur = max(scores, key=scores.get)
    return meilleur, scores


def probabilite_laplace(mot_precedent, mot):
    """Probabilité avec lissage de Laplace : plus aucune valeur nulle."""
    V = len(VOCAB)
    return (BI[(mot_precedent, mot)] + 1) / (UNI[mot_precedent] + V)



def predire_unigramme():
    """Modèle unigramme : prédit le mot le plus fréquent (aucun contexte)."""
    candidats = {mot: c for mot, c in UNI.items() if mot not in ("<s>", "</s>")}
    total = sum(candidats.values())
    candidats = {mot: c/total for mot, c in candidats.items()}
    return dict(sorted(candidats.items(), key=lambda x: x[1], reverse=True))


def predire_trigramme(contexte):
    """Modèle trigramme : prédit à partir des 2 mots précédents."""
    mots = contexte.lower().split()
    if len(mots) < 2:
        return {}
    avant_avant, avant = mots[-2], mots[-1]
    candidats = {}
    for (a, b, c), compte in TRI.items():
        if a == avant_avant and b == avant:
            # P(c | a, b) = C(a,b,c) / C(a,b)
            candidats[c] = compte / BI[(a, b)]
    return dict(sorted(candidats.items(), key=lambda x: x[1], reverse=True))


