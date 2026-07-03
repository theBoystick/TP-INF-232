import unicodedata

def normaliser_nom(nom_chef):
    texte=nom_chef.upper()
    texte=''.join(
        caractere for caractere in unicodedata.normalize('NFD', texte)
        if unicodedata.category(caractere) != 'Mn'
    )
    texte=''.join(
        caractere for caractere in texte
        if caractere.isalnum() or caractere.isspace()
    )
    return texte

def generer_graine(chaine):
    seed=0
    modulo=2147483647
    for position, caractere in enumerate(chaine, start=1):
        if 'A' <= caractere <= 'Z':
            valeur=ord(caractere)-ord('A')+1
        else:
            valeur=0

        seed=(seed*37+position*valeur)%modulo
    return seed


nom_chef="KENGNE GUEPOUOKSI Pierre Josué"
chaine_normalisee=normaliser_nom(nom_chef)
GRAINE=generer_graine(chaine_normalisee)

print("Chaine utilisée :", chaine_normalisee)
print("Graine du groupe :", GRAINE)
