# Sorbonne Université 3I024 2024-2025
# TME 2 : Cryptanalyse du chiffre de Vigenere
#
# Etudiant.e 1 : EL BOUKILI 21210507
# Etudiant.e 2 : EL HADDAD 21215054

import sys, getopt, string, math

# Alphabet français
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Fréquence moyenne des lettres en français
# À modifier
freq_FR = [0.09213414037491088,0.010354463742221126,0.030178915678726964,0.03753683726285317,0.17174710607479665,0.010939030914707838,0.01061497737343803,0.010717912027723734,0.07507240372750529,0.003832727374391129,6.989390105819367e-05,0.061368115927295096,0.026498684088462805,0.07030818127173859,0.049140495636714375,0.023697844853330825,0.010160031617459242,0.06609294363882899,0.07816806814528274,0.07374314880919855,0.06356151362232132,0.01645048271269667,1.14371838095226e-05,0.004071637436190045,0.0023001447439151006,0.0012263202640210343]

# Chiffrement César
def chiffre_cesar(txt, key):
    """
    Chiffre un texte en utilisant le chiffrement de César.

    Paramètres :
    txt (str) : Le texte à chiffrer (en majuscules sans espaces ni caractères spéciaux).
    key (int) : La clé de décalage, un entier représentant le nombre de positions à décaler dans l'alphabet.

    Retour :
    str : Le texte chiffré selon le chiffrement de César.
    """
    res = ""
    for char in txt:
        res += chr((ord(char) + key - ord('A')) % 26 + ord('A'))
    return res

# Déchiffrement César
def dechiffre_cesar(txt, key):
    """
    Déchiffre un texte chiffré avec le chiffrement de César.

    Paramètres :
    txt (str) : Le texte chiffré (en majuscules).
    key (int) : La clé de décalage utilisée pour chiffrer le texte.

    Retour :
    str : Le texte déchiffré en clair.
    """
    res = ""
    for char in txt:
        res += chr((ord(char) - key - ord('A')) % 26 + ord('A'))
    return res

# Chiffrement Vigenère
def chiffre_vigenere(txt, key):
    """
    Chiffre un texte en utilisant le chiffrement de Vigenère.

    Paramètres :
    txt (str) : Le texte à chiffrer (en majuscules sans espaces ni caractères spéciaux).
    key (list[int]) : Une liste d'entiers représentant la clé sous forme de décalages alphabétiques.

    Retour :
    str : Le texte chiffré selon le chiffrement de Vigenère.
    """
    i = 0
    res = ""
    for char in txt:
        if i == len(key):
            i = 0
        res += chr((ord(char) + key[i] - ord('A')) % 26 + ord('A'))
        i += 1
    return res

# Déchiffrement Vigenère
def dechiffre_vigenere(txt, key):
    """
    Déchiffre un texte chiffré avec le chiffrement de Vigenère.

    Paramètres :
    txt (str) : Le texte chiffré (en majuscules).
    key (list[int]) : Une liste d'entiers représentant la clé sous forme de décalages alphabétiques.

    Retour :
    str : Le texte déchiffré en clair.
    """
    i = 0
    res = ""
    for char in txt:
        if i == len(key):
            i = 0
        res += chr((ord(char) - key[i] - ord('A')) % 26 + ord('A'))
        i += 1
    return res

# Analyse de fréquences
def freq(txt):
    """
    Analyse la fréquence des lettres dans un texte donné.

    Paramètres :
    txt (str) : Le texte à analyser (en majuscules sans espaces ni caractères spéciaux).

    Retour :
    list[int] : Une liste de 26 éléments représentant la fréquence de chaque lettre de l'alphabet.
                L'index 0 correspond à 'A', 1 à 'B', ..., 25 à 'Z'.
    """
    occurrences = [0] * 26
    for char in txt:
        indice = ord(char) - ord('A')
        occurrences[indice] += 1
    return occurrences

# Renvoie l'indice dans l'alphabet de la lettre la plus fréquente d'un texte
def lettre_freq_max(txt):
    """
    Détermine la lettre la plus fréquente dans un texte et renvoie son indice dans l'alphabet.

    Paramètres :
    txt (str) : Le texte à analyser (en majuscules sans espaces ni caractères spéciaux).

    Retour :
    int : L'indice de la lettre la plus fréquente dans l'alphabet ('A' correspond à 0, ..., 'Z' correspond à 25).
    """
    occurrences = freq(txt)
    return occurrences.index(max(occurrences))

# Indice de coïncidence
def indice_coincidence(hist):
    """
    Calcule l'indice de coïncidence d'un texte à partir de son histogramme de fréquences.

    Paramètres :
    hist (list[int]) : Une liste de 26 éléments représentant la fréquence de chaque lettre de l'alphabet.

    Retour :
    float : L'indice de coïncidence du texte, qui mesure la probabilité que deux lettres choisies au hasard soient identiques.
    """
    N = sum(hist)  
    somme = 0

    for freq in hist:
        somme += (freq * (freq - 1))

    indice = somme / (N * (N - 1))
    return indice

# Recherche la longueur de la clé
def longueur_clef(cipher):
    """
    Estime la longueur de la clé utilisée pour chiffrer un texte avec le chiffrement de Vigenère.

    Paramètres :
    cipher (str) : Le texte chiffré (en majuscules sans espaces ni caractères spéciaux).

    Retour :
    int : La longueur estimée de la clé. Retourne 0 si aucune longueur probable n'est trouvée.
    """
    # Tester des longueurs de clé de 4 à 20
    for k in range(4, 21):
        colonnes = ['' for _ in range(k)]

        # Découper le texte en k colonnes
        for i, char in enumerate(cipher):
            colonnes[i % k] += char

        # Calculer l'IC de chaque colonne
        Tab_indices = []
        for colonne in colonnes:
            hist = freq(colonne)
            IC = indice_coincidence(hist)
            Tab_indices.append(IC)

        # Calculer la moyenne des IC
        moyenne_IC = sum(Tab_indices) / len(Tab_indices)

        if moyenne_IC > 0.06:  
            return k  
    return 0

    
# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en utilisant la lettre la plus fréquente
# de chaque colonne
def clef_par_decalages(cipher, key_length):
    """
    Détermine les décalages de la clé de chiffrement de Vigenère en se basant sur la fréquence maximale des lettres.

    Paramètres :
    cipher (str) : Le texte chiffré (en majuscules sans espaces ni caractères spéciaux).
    key_length (int) : La longueur estimée de la clé.

    Retour :
    list[int] : Une liste d'entiers représentant les décalages de la clé pour chaque position.
    """
    groupes = ['' for _ in range(key_length)]  
    for i, lettre in enumerate(cipher):
        groupes[i % key_length] += lettre  

    decalages = []
    for txt in groupes:
        char_max = lettre_freq_max(txt) + ord('A') % 26  # Détermine la lettre la plus fréquente
        decalage = (char_max - ord('E')) % 26  # Suppose que la lettre la plus fréquente correspond à 'E'
        decalages.append(decalage)
    return decalages

# Cryptanalyse V1 avec décalages par fréquence max
def cryptanalyse_v1(cipher):
    """
    Déchiffre un texte chiffré avec Vigenère en utilisant une attaque par analyse de fréquences.

    Paramètres :
    cipher (str) : Le texte chiffré (en majuscules sans espaces ni caractères spéciaux).

    Retour :
    str : Le texte déchiffré.
    """
    lc = longueur_clef(cipher)  # Estime la longueur de la clé
    clef = clef_par_decalages(cipher, lc)  # Déduit la clé par analyse de fréquence
    res = dechiffre_vigenere(cipher, clef)  # Déchiffre le texte
    return res
    
    """ Pour la fonction clef_par_decalage on a supposé que la lettre la 
    plus frequente c'est E mais c'est pas toujours le cas""" 


################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V2.

# Indice de coincidence mutuelle avec décalage
def indice_coincidence_mutuelle(h1, h2, d):
    """
    Calcule l'indice de coïncidence mutuelle entre deux distributions de fréquences.

    Paramètres :
    h1 (list[int]) : Histogramme de fréquence du premier texte (référence).
    h2 (list[int]) : Histogramme de fréquence du deuxième texte.
    d (int) : Décalage appliqué au deuxième histogramme pour tester l'alignement.

    Retour :
    float : L'indice de coïncidence mutuelle entre les deux distributions.
    """
    i = 0
    res = 0.0
    while i < len(h1):
        res += h1[i] * h2[(i + d) % 26] 
        i += 1
    return res / (sum(h1) * sum(h2))

# Renvoie le tableau des décalages probables étant
# donné la longueur de la clé
# en comparant l'indice de coïncidence mutuelle par rapport
# à la première colonne
def tableau_decalages_ICM(cipher, key_length):
    """
    Détermine les décalages de la clé en utilisant l'indice de coïncidence mutuelle.

    Paramètres :
    cipher (str) : Le texte chiffré (en majuscules sans espaces ni caractères spéciaux).
    key_length (int) : La longueur estimée de la clé.

    Retour :
    list[int] : Une liste de décalages pour chaque position de la clé.
    """
    tab_div = ['' for _ in range(key_length)]  
    for i, lettre in enumerate(cipher):
        tab_div[i % key_length] += lettre  

    referenciel = tab_div[0]  # Première colonne comme référence

    freq_ref = freq(referenciel)  
    decalages = [0] * key_length  

    for i in range(1, key_length):  
        freq_i = freq(tab_div[i])  
        
        meilleur_decalage = 0
        meilleur_icm = 0
        for d in range(26):
            icm = indice_coincidence_mutuelle(freq_ref, freq_i, d)
            if icm > meilleur_icm:
                meilleur_icm = icm
                meilleur_decalage = d

        decalages[i] = meilleur_decalage

    return decalages

# Cryptanalyse V2 avec décalages par ICM
def cryptanalyse_v2(cipher):
    """
    Déchiffre un texte chiffré avec Vigenère en utilisant une analyse basée sur l'indice de coïncidence mutuelle.

    Paramètres :
    cipher (str) : Le texte chiffré (en majuscules sans espaces ni caractères spéciaux).

    Retour :
    str : Le texte déchiffré.
    """
    lc = longueur_clef(cipher)  # Estimation de la longueur de la clé
    tab_ICM = tableau_decalages_ICM(cipher, lc)  # Calcul des décalages via ICM

    tab_div = ['' for _ in range(lc)]
    for i, lettre in enumerate(cipher):
        tab_div[i % lc] += lettre  

    # Déchiffrement colonne par colonne avec les décalages trouvés
    txt_dechiffre_colonnes = [dechiffre_cesar(tab_div[i], tab_ICM[i]) for i in range(lc)]

    # Reconstruction du texte clair à partir des colonnes déchiffrées
    txt_clair = ""
    for i in range(len(cipher)):
        txt_clair += txt_dechiffre_colonnes[i % lc][i // lc]

    char_max = lettre_freq_max(txt_clair)  # Trouver la lettre la plus fréquente
    decalage_final = (char_max - (ord('E') - ord('A'))) % 26  # Ajustement final

    return dechiffre_cesar(txt_clair, decalage_final)

    """ Il y'a 45 textes qui ont étaient déchiffrés. Ont a utilisé les ICM pour savoir les décalages 
    il peux y avoir des décalages qui sont pas précis ou peut etre les textes sont pas en francais vue 
    qu'on a utilisé E comme lettre la plus frequente"""



################################################################


### Les fonctions suivantes sont utiles uniquement
### pour la cryptanalyse V3.

# Prend deux listes de même taille et
# calcule la correlation lineaire de Pearson
def correlation(L1, L2):
    """
    Calcule le coefficient de corrélation de Pearson entre deux listes de valeurs.

    Paramètres :
    L1 (list[float]) : Première liste de valeurs numériques.
    L2 (list[float]) : Deuxième liste de valeurs numériques.

    Retour :
    float : Le coefficient de corrélation de Pearson entre L1 et L2.
            Une valeur proche de 1 indique une forte corrélation positive,
            proche de -1 une forte corrélation négative, et proche de 0 aucune corrélation.
    
    Remarque :
    Cette fonction suppose que L1 et L2 ont la même longueur et contiennent au moins deux éléments.
    """
    haut = 0.0  # Numérateur de la formule
    bas1 = 0.0  # Partie du dénominateur liée à L1
    bas2 = 0.0  # Partie du dénominateur liée à L2
    i = 0 

    while i < len(L1):  
        moyenne_L1 = sum(L1) / len(L1)
        moyenne_L2 = sum(L2) / len(L2)
        
        haut += (L1[i] - moyenne_L1) * (L2[i] - moyenne_L2)
        bas1 += (L1[i] - moyenne_L1) ** 2
        bas2 += (L2[i] - moyenne_L2) ** 2
        i += 1  
    
    return haut / (math.sqrt(bas1 * bas2))



# Renvoie la meilleur clé possible par correlation
# étant donné une longueur de clé fixée
def clef_correlations(cipher, key_length):
    """
    Détermine la clé probable utilisée pour chiffrer un texte avec Vigenère en analysant 
    la corrélation entre les fréquences de lettres du texte et celles de la langue française.

    Paramètres :
    cipher (str) : Le texte chiffré en majuscules sans espaces ni caractères spéciaux.
    key_length (int) : La longueur supposée de la clé.

    Retour :
    tuple(float, list[int]) : 
      - `score` (float) : Moyenne des meilleures corrélations trouvées pour chaque colonne.
      - `decalages` (list[int]) : Liste des décalages correspondant aux lettres de la clé estimée.

    """
    # Diviser le texte chiffré en `key_length` parties (colonnes)
    tab_div = ['' for _ in range(key_length)]  
    for i, lettre in enumerate(cipher):
        tab_div[i % key_length] += lettre  

    decalages = [0] * key_length  
    res = 0.0

    for i in range(key_length):  
        meilleur_decalage = 0
        meilleur_cor = 0

        for d in range(26): 
            txt_dec = dechiffre_cesar(tab_div[i], d)  # Tester le décalage d
            freq_i = freq(txt_dec)  # Calculer la fréquence des lettres du texte déchiffré
            cor = correlation(freq_FR, freq_i)  # Comparer avec la fréquence française

            if cor > meilleur_cor:  # Garder le décalage avec la meilleure corrélation
                meilleur_cor = cor
                meilleur_decalage = d

        res += meilleur_cor
        decalages[i] = meilleur_decalage

    score = res / key_length  # Calculer la moyenne des meilleures corrélations
    return score, decalages


# Cryptanalyse V3 avec correlations
def cryptanalyse_v3(cipher):
    """
    Déchiffre un texte chiffré avec Vigenère en utilisant une analyse par corrélation.

    Paramètres :
    cipher (str) : Le texte chiffré (en majuscules sans espaces ni caractères spéciaux).

    Retour :
    str : Le texte déchiffré.
    """
    cor = -1 
    meilleur_decalage = []  

    for taille in range(1, 21):  # Tester les longueurs de clé de 1 à 20
        moyenne_corr, decalages = clef_correlations(cipher, taille)

        if moyenne_corr > cor:  # Sélectionner la clé avec la meilleure corrélation
            cor = moyenne_corr
            meilleur_decalage = decalages

    txt = dechiffre_vigenere(cipher, meilleur_decalage)  
    return txt
    """Si une clé est trop longue par rapport à la taille du texte, le calcul de correlation ne sera pas bon 
    puisqu'on se base sur la frequence des lettres les plus frequentes alors si l'echantillon ou on extrait 
    les frequence est trop petit le resultat ne sera pas bon"""



################################################################
# NE PAS MODIFIER LES FONCTIONS SUIVANTES
# ELLES SONT UTILES POUR LES TEST D'EVALUATION
################################################################


# Lit un fichier et renvoie la chaine de caracteres
def read(fichier):
    f=open(fichier,"r")
    txt=(f.readlines())[0].rstrip('\n')
    f.close()
    return txt

# Execute la fonction cryptanalyse_vN où N est la version
def cryptanalyse(fichier, version):
    cipher = read(fichier)
    if version == 1:
        return cryptanalyse_v1(cipher)
    elif version == 2:
        return cryptanalyse_v2(cipher)
    elif version == 3:
        return cryptanalyse_v3(cipher)

def usage():
    print ("Usage: python3 cryptanalyse_vigenere.py -v <1,2,3> -f <FichierACryptanalyser>", file=sys.stderr)
    sys.exit(1)

def main(argv):
    size = -1
    version = 0
    fichier = ''
    try:
        opts, args = getopt.getopt(argv,"hv:f:")
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-v"):
            version = int(arg)
        elif opt in ("-f"):
            fichier = arg
    if fichier=='':
        usage()
    if not(version==1 or version==2 or version==3):
        usage()

    print("Cryptanalyse version "+str(version)+" du fichier "+fichier+" :")
    print(cryptanalyse(fichier, version))
    
if __name__ == "__main__":
   main(sys.argv[1:])
