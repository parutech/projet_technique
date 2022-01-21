from PTF import *
import datetime

dateActuelle
listeObjetsActions

if (__name__ == '__main__') :
    filePath = os.getcwd() + '\\ListeSymboles.txt'
    if (os.path.exists(filePath) == False) :
        WebScraping.CreerListeSymboles()
    with open('ListeSymboles.txt', 'r') as file :
        lines = file.readlines()
        for line in lines :
            action = Action(line.strip().split(';')[0])
            listeObjetsActions.append(action)

print(listeObjetsActions)

dates, donnees = listeObjetsActions[0].getDonneesGraphiques('2W')

print(dates)
print(donnees)