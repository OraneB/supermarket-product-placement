import random
import pandas as pd

dico_rayons = {"Fruits et Légumes" : ["Pommes", "Salade verte",  "Tomates", "Pommes de terre", "Carottes", "Oignons", "Concombres"],
               "Crèmerie" : ["Lait", "Oeufs", "Farine", "Sucre"], "Produits laitiers" : ["Yaourts", "Fromage rapé", "Fromage", "Crème fraiche", "Beurre"],
               "Boulangerie" : ["Pain", "Viennoiseries"], "Boucherie" : ["Poulet", "Jambon", "Steak Haché", "Saucisses"],
               "Epicerie" : ["Pâtes", "Riz", "Lentilles"], "Condiment" : ["Huile d'olive", "Sel"],
               "Boisson" : ["Eau", "Jus de fruits"], "Petit-déjeuner" : ["Café", "Céréales", "Thé"], "Conserves" : ["Thon", "Légumes en conserve"],
               "Produits d'hygiène" : ["Papier toilette", "Savon", "Dentifrice"], "Produits ménagers" : ["Lessive", "Liquide vaisselle"],
               "Epicerie sucré" : ["Biscuits", "Chocolat"], "Biscuits salés" : ["Chips"], "Surgelés" : ["Pizzas", "Légumes congelés"]}
liste_rayons = ["Fruits et Légumes", "Crèmerie", "Produits laitiers", "Boulangerie", "Boucherie", "Epicerie", "Condiment", "Boisson", "Petit-déjeuner",
                "Conserves", "Produits d'hygiène", "Produits ménagers", "Epicerie sucré", "Biscuits salés", "Surgelés"]
liste_produits = ["Pommes", "Salade verte",  "Tomates", "Pommes de terre", "Carottes", "Oignons", "Concombres", "Lait", "Oeufs", "Farine", "Sucre", "Yaourts", "Fromage rapé",
                  "Fromage", "Crème fraiche", "Beurre", "Pain", "Viennoiseries", "Poulet", "Jambon", "Steak Haché", "Saucisses", "Pâtes", "Riz", "Lentilles", "Huile d'olive", "Sel", "Eau",
                  "Jus de fruits", "Café", "Céréales", "Thé", "Thon", "Légumes en conserve", "Papier toilette", "Savon", "Dentifrice", "Lessive", "Liquide vaisselle", "Biscuits", "Chocolat",
                  "Chips", "Pizzas", "Légumes congelés"]
N_rayons = 15
N_produits = 44
N_supermarche = 4
# le supermarché est une matrice 4*4 et en [0][0] on a l'entrée, sortie, caisses
fichier_achat = pd.read_csv('probabilites_achats_supermarche.csv', sep=';', index_col=0) #ouverture du fichier csv contenant les probas d'achat
fichier_proba_produits = pd.read_csv('probabilites_produits.csv', sep=';', index_col=0) #ouverture du fichier csv contenant les probas d'avoir le produit dans une liste
fichier_prix_produits = pd.read_csv('prix_moyens_produits.csv', sep=';', index_col=0)


def init_supermarche() :
  # initialise un supermarche vide
  return [N_supermarche*[-1] for i in range(N_supermarche)]

def proba_rayons():
  # renvoie une matrice N_rayons*N_rayons où la case i j represente le pourcentage de chance d'acheter qqe chose dans le rayon j sachant q'un produit a été acheté dans le rayon i 
  dist = [N_rayons*[0] for i in range(N_rayons)]
  for i in range (N_rayons):
    for j in range(N_rayons):
      r1 = liste_rayons[i]
      r2 = liste_rayons[j]
      for art_ach in dico_rayons.get(r1):
        for art_prob in dico_rayons.get(r2):
          dist[i][j] += fichier_achat.loc[art_ach, art_prob]
      dist[i][j] = dist[i][j] / (len(dico_rayons.get(r1)) * len(dico_rayons.get(r2)))
  return [[round(float(x), 2) for x in row] for row in dist] #enleve np.float pour remettre en float

def ponderation_rayons():
  l = [0 for i in range(N_rayons)]
  for i in range(N_rayons):
    for prod in dico_rayons.get(liste_rayons[i]):
      l[i] += fichier_proba_produits.loc[prod, 'Probabilité_liste_courses_%']
  return [int(x) for x in l]

def indice_max(l):
  i_max = 0
  for i in range(1, N_rayons):
    if l[i] > l[i_max]:
      i_max = i
  return i_max

def supprimer(matrice_prob, ind):
  for i in range (N_rayons):
    matrice_prob[i][ind] = -1

### Organisation des supermarchés

def organisation_aleatoire(): # mélange de Knuth
  ind = [i for i in range(N_rayons)]
  for i in range(N_rayons):
    k = random.randint(0, i)
    tmp = ind[k]
    ind[k] = ind[i]
    ind[i] = tmp
  supermarche = init_supermarche()
  for i in range(1, 16):
    l = i//N_supermarche #ligne dans la matrice
    k= i%N_supermarche #colonne dans la matrice
    supermarche[l][k] = ind[i - 1]
  return supermarche

def remplir_proche(supermarche, i, j, prob):
  if i == 0: #si i = 0 on s'arrete un j avant
    if j > 1:
      liste_proba1 = prob[supermarche[i][j]]
      liste_proba2 = prob[supermarche[i + 1][j - 1]]
      liste_tot = [liste_proba1[i] + liste_proba2[i] for i in range(N_rayons)]
      ind = indice_max(liste_tot)
      supprimer(prob, ind)
      supermarche[i][j-1] = ind
      remplir_proche(supermarche, i, j - 1, prob)
  elif i == 3: #si j = 3 on doit aussi remonter
    if j > 0:
      ind1= indice_max(prob[i])
      supprimer(prob, ind1)
      supermarche[i][j-1] = ind1
      remplir_proche(supermarche, i, j - 1, prob) #commence par remplir le bas
    if j == 3:
      ind2 = indice_max(prob[i])
      supprimer(prob, ind2)
      supermarche[i-1][j] = ind2
      remplir_proche(supermarche, i - 1, j, prob)
  else:
    if j > 0:
      liste_proba1 = prob[supermarche[i][j]]
      liste_proba2 = prob[supermarche[i + 1][j - 1]]
      liste_tot = [liste_proba1[i] + liste_proba2[i] for i in range(N_rayons)]
      ind = indice_max(liste_tot)
      supprimer(prob, ind)
      supermarche[i][j-1] = ind
      remplir_proche(supermarche, i, j - 1, prob)
    if j == 3:
      ind2 = indice_max(prob[i])
      supprimer(prob, ind2)
      supermarche[i-1][j] = ind2
      remplir_proche(supermarche, i - 1, j, prob)
 
def organisation_proche1():
  supermarche = init_supermarche()
  r_max_ponderation = indice_max(ponderation_rayons())
  matrice_probas = proba_rayons()
  supermarche[3][3] = r_max_ponderation
  supprimer(matrice_probas, r_max_ponderation)
  remplir_proche(supermarche, 3, 3, matrice_probas)
  return supermarche

def organisation_proche():
  supermarche = init_supermarche()
  r_max_ponderation = indice_max(ponderation_rayons())
  matrice_probas = proba_rayons()
  supermarche[-1][-1] = r_max_ponderation
  supprimer(matrice_probas, r_max_ponderation)
  a_remplir = [(N_supermarche - 1, N_supermarche - 2), (N_supermarche - 2, N_supermarche - 1)]
  while a_remplir != []:
    (i,j) = a_remplir.pop(0)
    if i == N_supermarche - 1 :
      ind = indice_max(matrice_probas[supermarche[i][j + 1]])
      supprimer(matrice_probas, ind)
      supermarche[i][j] = ind
      if j > 0:
        a_remplir.append((i, j-1))
      elif j == N_supermarche - 1:
        ind = indice_max(matrice_probas[supermarche[i + 1][j]])
        supprimer(matrice_probas, ind)
        supermarche[i][j] = ind
        a_remplir.append((i, j - 1))
        if i != 0:
          a_remplir.append((i - 1, j))
      else :
        liste_proba1 = matrice_probas[supermarche[i][j + 1]]
        liste_proba2 = matrice_probas[supermarche[i + 1][j]]
        liste_tot = [liste_proba1[k] + liste_proba2[k] for k in range(N_rayons)]
        ind = indice_max(liste_tot)
        supprimer(matrice_probas, ind)
        supermarche[i][j] = ind
        if j > 0 and not(i == 0 and j == 1):
          a_remplir.append((i, j - 1))
  return supermarche

def liste_indices_dispo(supermarche, i, j):
  l = []
  for k in range(N_supermarche):
    if i != 0 and supermarche[i][k] == -1:
      l.append((i,k))
    if i == 0 and k != 0 and supermarche[i][k] == -1:
      l.append((i,k))
    if j != 0 and supermarche[k][j] == -1:
      l.append((k,j))
    if j == 0 and k != 0 and supermarche[k][j] == -1:
      l.append((k,j))
  return l

def dist(i, j, k, l) :
  # return abs( i - k + j - l) (truc d'origine)
  return abs(i - k) + abs(j - l)

def liste_ind_dist_max(supermarche, i, j):
  lst = liste_indices_dispo(supermarche, i, j)
  res = []
  if lst != []:
    (p,q) = lst[0]
    dist_max = dist(i, j, p, q)
    for (p,q) in lst:
      d = dist(i, j, p, q)
      if  d > dist_max:
        res = [(p,q)]
        dist_max = d
      elif d == dist_max:
        res.append((p,q))
  return res


def organisation_loin():
  supermarche = init_supermarche()
  r_max_ponderation = indice_max(ponderation_rayons())
  matrice_probas = proba_rayons()
  supermarche[-1][-1] = r_max_ponderation
  supprimer(matrice_probas, r_max_ponderation)
  a_voir = liste_ind_dist_max(supermarche, N_supermarche - 1, N_supermarche - 1)
  for (p,q) in a_voir:
    ind = indice_max(matrice_probas[supermarche[-1][-1]])
    supprimer(matrice_probas, ind)
    supermarche[p][q] = ind
  while a_voir != [] :
    (i,j) = a_voir.pop(0)
    lst = liste_ind_dist_max(supermarche, i, j)
    for (p,q) in lst:
      ind = indice_max(matrice_probas[supermarche[i][j]])
      supprimer(matrice_probas, ind)
      supermarche[p][q] = ind
      a_voir.append((p,q))
  return supermarche



### visite du supermarche

def generation_liste(nb_clients):
  listes = []
  probas = fichier_proba_produits['Probabilité_liste_courses_%']
  for _ in range(nb_clients):
    l = [produit for produit, p in probas.items() if random.randint(0, 99) < p]
    while l == []: #pour éviter d'avoir une liste de course vide 
      l = [produit for produit, p in probas.items() if random.randint(0, 99) < p]
      listes.append(l)
    listes.append(l)
  return listes
    
def generation_probas_achats_pour_liste (liste_course):
  l = {}
  if liste_course != []:
    for produit in liste_produits:
      if produit in liste_course:
        l[produit] = 100
      else:
        somme = 0
        for produit_achete in liste_course:
          somme += int(fichier_achat[produit_achete][produit])
        l[produit] = int(somme / len(liste_course))
  return l

def trouver_indice (supermarche, rayon):
  for i in range(len(supermarche)):
    for j in range(len(supermarche[0])):
      if supermarche[i][j] == rayon:
        return (i,j)

def rayon_par_article():
  dic = {}
  for rayon, produits in dico_rayons.items():
    for produit in produits:
      dic[produit] = liste_rayons.index(rayon)
  return dic

def chemin_explore(i, j, k, l):
  deja_visite = [[False]*N_supermarche for _ in range(N_supermarche)]
  file = [ (i, j, [(i, j)]) ]  # file d'attente : chaque élément = (x, y, chemin_parcouru)
  deja_visite[i][j] = True
  while file != []:
    x, y, path = file.pop(0)  # Retire le premier élément de la file (FIFO)
    if (x, y) == (k, l):
      return path  # On a trouvé la cible, on retourne le chemin
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
      new_x, new_y = x + dx, y + dy
      if 0 <= new_x < N_supermarche and 0 <= new_y < N_supermarche and not deja_visite[new_x][new_y]:
        deja_visite[new_x][new_y] = True
        file.append( (new_x, new_y, path + [(new_x, new_y)]) )
  return []  # Aucun chemin trouvé

def simulation_achat(supermarche, liste, dico_articles_rayons):
  depense = 0
  liste_copie = liste[:]
  produit_achete = []
  i_actuel, j_actuel = 0, 0
  probas_achat_produit = generation_probas_achats_pour_liste(liste_copie)
  while liste_copie != []:
    rayon_vise = dico_articles_rayons.get(liste_copie.pop(0))
    i_rayon, j_rayon = trouver_indice(supermarche, rayon_vise)
    chemin = chemin_explore(i_actuel, j_actuel, i_rayon, j_rayon)
    for i,j in chemin:
      for produit in dico_rayons.get(liste_rayons[supermarche[i][j]]):
        if not(produit in produit_achete):
          if random.randint(0, 99) < probas_achat_produit.get(produit):
            depense += fichier_prix_produits.loc[produit, 'Prix_moyen_euros']
            produit_achete.append(produit)
          else :
            probas_achat_produit[produit] = probas_achat_produit.get(produit) * 0.5
          if produit in liste_copie:
            ind = liste_copie.index(produit)
            liste_copie.pop(ind)
    i_actuel, j_actuel = i_rayon, j_rayon
  chemin = chemin_explore(i_actuel, j_actuel, 0, 0)
  for i,j in chemin:
    for produit in dico_rayons.get(liste_rayons[supermarche[i][j]]):
      if not(produit in produit_achete):
        if random.randint(0, 99) < probas_achat_produit.get(produit):
          depense += fichier_prix_produits.loc[produit, 'Prix_moyen_euros']
  return round(float(depense), 2)


### Comparaison des résultats

def magasin_plus_rapportant(nombre_essais, supermarche_aleatoire, supermarche_proche, supermarche_loin):
  liste_des_listes = generation_liste(nombre_essais)
  somme_alea = 0
  somme_proche = 0
  somme_loin = 0
  dico_articles_rayons = rayon_par_article()
  for i in range(nombre_essais):
    somme_alea += simulation_achat(supermarche_aleatoire, liste_des_listes[i], dico_articles_rayons)
    somme_proche += simulation_achat(supermarche_proche, liste_des_listes[i], dico_articles_rayons)
    somme_loin += simulation_achat(supermarche_loin, liste_des_listes[i], dico_articles_rayons)
  moyenne_alea = round(somme_alea/nombre_essais, 2)
  moyenne_proche = round(somme_proche/nombre_essais, 2)
  moyenne_loin = round(somme_loin/nombre_essais, 2)
  print(f"Aléatoire : {moyenne_alea}, Proche : {moyenne_proche}, Loin : {moyenne_loin}")


for _ in range(10):
  alea = organisation_aleatoire()
  print(alea)
  magasin_plus_rapportant(100, alea, organisation_proche(), organisation_loin())
  print("\n")
