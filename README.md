# Cryptanalyse du chiffrement de Vigenère

## 📜 Présentation
L'objectif de ce projet est d'implémenter plusieurs outils permettant de cryptanalyser un texte chiffré avec le chiffrement de Vigenère. Le projet est principalement développé en Python.

## 📌 Objectifs

À la fin du projet, le programme devra être capable de :

- Chiffrer et déchiffrer un texte avec le chiffre de César et Vigenère.
- Déterminer la taille de la clé à l'aide de différentes approches :
  - Indice de coïncidence
  - Indice de coïncidence mutuelle
  - Corrélation de Pearson
- Retrouver la clé et déchiffrer le texte chiffré.
- Implémenter trois méthodes de cryptanalyse :
  - `cryptanalyse_v1` : basée sur l'indice de coïncidence
  - `cryptanalyse_v2` : utilisant l'indice de coïncidence mutuelle
  - `cryptanalyse_v3` : exploitant la corrélation de Pearson

## 🚀 Utilisation

### Lancer les tests
Les tests sont fournis et permettent de valider chaque étape du projet. 
Pour exécuter un test :
```bash
python3 test-1-cesar.py
```

Chaque test valide une fonctionnalité spécifique :

- `test-1-cesar.py` : chiffrement/déchiffrement César
- `test-2-vigenere.py` : chiffrement/déchiffrement Vigenère
- `test-3-indice-coincidence.py` : calcul de l'indice de coïncidence
- ...

## 🛠️ Structure du projet

```
.
├── README.md
├── cryptanalyse_vigenere.py
│── test-1-cesar.py
│── test-2-vigenere.py
└── data/
    └── texte_chiffre.txt
```

- `cryptanalyse_vigenere.py` : contient toutes les fonctions implémentées (chiffrement, déchiffrement, analyse de fréquences, etc.)
- `tests-?-???` : tests pour valider chaque étape
- `data/` : fichiers textes pour les tests
