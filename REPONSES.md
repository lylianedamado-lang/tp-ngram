# Réponses aux questions du TP - Modèles N-grammes

Lyliane Fat-Nelle Généviève Damado

## Partie 1 - Prétraitement

- **Taille du vocabulaire :** 15 mots différents (marqueurs `<s>` et `</s>` compris).
- **Nombre total de tokens :** 45.
- **Différence vocabulaire / tokens :** le vocabulaire compte chaque mot **une seule fois** (les mots distincts), alors que le nombre de tokens compte **toutes les occurrences**, répétitions comprises. Le mot " le " apparaît plusieurs fois dans les tokens, mais une seule fois dans le vocabulaire.

## Partie 2 - N-grammes

- **Bigramme le plus fréquent :** `(<s>, le)`, qui apparaît 6 fois, car les six phrases commencent par " le ".
- **Trigramme le plus fréquent :** `(<s>, le, chat)`, 3 fois.

## Partie 3 - Modèle bigramme

1. **Pourquoi certaines probabilités sont-elles nulles ?** Parce que le bigramme correspondant n'apparaît jamais dans le corpus : son comptage est 0, donc la probabilité est 0.
2. **Une probabilité élevée ?** Le deuxième mot suit très souvent le premier ; c'est un enchaînement fréquent dans le corpus (ex. après " du ", toujours " poisson ").
3. **Une probabilité nulle ?** Cet enchaînement de deux mots n'a jamais été observé dans le corpus.

## Partie 4 - Prédiction

**Différence entre P(chat | le) et P(le | chat).** P(chat | le) mesure la chance de voir " chat " **après** " le ". P(le | chat) mesure la chance de voir " le " **après** " chat ". L'ordre est différent, donc ce sont deux bigrammes différents, `(le, chat)` et `(chat, le)`. Dans le corpus " le chat " existe mais " chat le " non, d'où des probabilités différentes. En général P(A|B) != P(B|A).

## Partie 5 - Génération

**Pourquoi les phrases générées peuvent-elles être incorrectes ou peu naturelles ?** Parce que le modèle bigramme ne regarde que le **mot précédent**. Il n'a aucune vision globale de la phrase ni de la grammaire. Il enchaîne des mots localement probables, mais l'ensemble peut ne pas avoir de sens. De plus, en prenant toujours le mot le plus probable, il génère toujours la même phrase.

## Partie 6 - Probabilité d'une phrase

**Que signifie une probabilité élevée pour une phrase ?** Que la phrase est **typique du corpus** : elle enchaîne des mots qui se suivent souvent dans les données d'apprentissage. Une phrase bien formée selon le corpus aura une probabilité plus élevée qu'une phrase inhabituelle.

## Partie 7 - Comparaison de phrases

**Comment les N-grammes tiennent-ils compte de l'ordre des mots ?** Ils ne comptent pas les mots isolément, mais les **paires ordonnées** de mots. `(le, chat)` et `(chat, le)` sont deux bigrammes distincts. Changer l'ordre change les bigrammes, donc la probabilité. C'est pourquoi " le chat mange du poisson " a une probabilité positive alors que " poisson le mange chat du " tombe à zéro.

## Partie 8 - Correction contextuelle

**Pourquoi les N-grammes détectent des erreurs qu'un dictionnaire ne peut pas voir ?** Un dictionnaire vérifie seulement si un mot **existe**. Or " cet " et " ans " existent tous les deux : l'erreur " Il a cet ans " n'est pas un mot inconnu, c'est un problème de **contexte**. Le N-gramme regarde le mot précédent : après " a ", " sept " est bien plus probable que " cet ". Il détecte donc une erreur contextuelle invisible pour un simple dictionnaire.

## Partie 9 - Comptes nuls

Plusieurs bigrammes ont une fréquence nulle, par exemple `(chat, pain)`, `(chien, poisson)`, `(mange, chien)`. **Le problème :** comme la probabilité d'une phrase est un **produit** de probabilités, un seul bigramme à 0 rend toute la phrase égale à 0. Le modèle juge alors " impossible " une phrase qui est simplement absente du corpus.

## Partie 10 - Lissage de Laplace

1. **Pourquoi +1 au numérateur ?** Pour qu'un bigramme jamais vu ait une probabilité non nulle (au moins 1 au lieu de 0). On fait comme si on avait vu chaque enchaînement une fois de plus.
2. **Pourquoi +V au dénominateur ?** Parce qu'on a ajouté 1 à chacun des V mots possibles du vocabulaire ; il faut donc ajouter V au total pour rester cohérent.
3. **Pourquoi modifier le dénominateur ?** Pour que la somme de toutes les probabilités reste égale à 1, c'est-à-dire pour conserver une vraie distribution de probabilité.

## Partie 11 - Comparaison des modèles

1. **Le moins de contexte ?** L'unigramme (aucun contexte, il ne regarde aucun mot précédent).
2. **Le plus de contexte ?** Le trigramme (il regarde les deux mots précédents).
3. **Pourquoi le trigramme est plus précis ?** Plus de contexte = prédiction plus spécifique, donc généralement plus pertinente.
4. **Pourquoi plus sensible aux comptes nuls ?** Les suites de trois mots sont bien plus rares que les paires ; beaucoup de trigrammes n'apparaissent jamais, ce qui multiplie les probabilités nulles.
5. **Quand le corpus augmente ?** On observe davantage de N-grammes différents, les estimations deviennent plus fiables et le problème des comptes nuls diminue.

## Questions de synthèse

1. **Qu'est-ce qu'un modèle de langage ?** Un système qui attribue une probabilité à une séquence de mots, et qui estime la probabilité qu'un mot apparaisse après un contexte donné.
2. **Corpus vs vocabulaire ?** Le corpus est l'ensemble des textes d'apprentissage (toutes les phrases, avec répétitions). Le vocabulaire est l'ensemble des mots distincts qui y apparaissent.
3. **Unigramme, bigramme, trigramme ?** Ce sont des suites de 1, 2 ou 3 mots consécutifs. Ils utilisent respectivement 0, 1 et 2 mots de contexte.
4. **Pourquoi une probabilité conditionnelle ?** Parce que le modèle bigramme estime la probabilité d'un mot **sachant** le mot précédent : P(mot | mot précédent).
5. **Que signifie P(chat | le) ?** La probabilité que le mot " chat " apparaisse juste après le mot " le ".
6. **Pourquoi P(chat | le) != P(le | chat) ?** Parce que l'ordre des mots compte : ce sont deux enchaînements différents, avec des comptages différents dans le corpus.
7. **Comment prédire le mot suivant ?** En cherchant, parmi tous les mots, celui qui a la plus forte probabilité après le contexte donné (argmax de P(mot | contexte)).
8. **Comment générer une phrase ?** En partant de `<s>`, en prédisant le mot suivant le plus probable, en l'ajoutant, et en répétant jusqu'à `</s>`.
9. **Comment comparer deux phrases ?** En calculant la probabilité de chacune (produit des probabilités de leurs bigrammes) et en comparant les deux valeurs.
10. **Pourquoi les comptes nuls posent-ils problème ?** Parce qu'une seule probabilité nulle annule toute la probabilité d'une phrase (multiplication par zéro).
11. **Rôle du lissage de Laplace ?** Éviter les probabilités nulles en ajoutant 1 à chaque comptage, ce qui donne une petite probabilité même aux enchaînements jamais vus.
12. **Pourquoi un trigramme peut être plus performant qu'un bigramme ?** Parce qu'il utilise plus de contexte (deux mots au lieu d'un), ce qui affine la prédiction.
13. **Limites des N-grammes sur les textes longs ?** Le contexte reste court (1 ou 2 mots) : le modèle ne capte pas les dépendances entre mots éloignés. Le nombre de N-grammes explose et les comptes nuls se multiplient.

## Défi - Pourquoi GPT n'utilise pas simplement des N-grammes ?

Les modèles modernes comme GPT dépassent les N-grammes car ceux-ci ont des limites fortes : le **contexte est limité** (seulement 1 ou 2 mots précédents), le **nombre de N-grammes explose** quand le vocabulaire et N grandissent, la **généralisation est faible** (un enchaînement jamais vu reste à zéro même s'il est plausible), les **comptes nuls** sont fréquents, et surtout les N-grammes ne **capturent pas les dépendances longues** ni le **sens profond** du texte. Les modèles neuronaux, eux, apprennent des représentations continues des mots (embeddings) et utilisent des mécanismes d'attention capables de relier des mots très éloignés, ce qui leur donne une compréhension du contexte bien plus riche.
