import os
import requests
from bs4 import BeautifulSoup


# Récupération de la liste de toutes les actions présentes sur Euronext Paris
def CreerListeSymboles() :
    baseUrl = 'https://www.boursorama.com/bourse/actions/cotations/page-'
    nombrePages = 0

    reponse = requests.get(baseUrl + "1")
    if (reponse.ok) :
        soup = BeautifulSoup(reponse.text, 'lxml')
        lienDernierePage = soup.findAll('a', {'aria-label' : 'Dernière page'})
        if (len(lienDernierePage) == 0) :
            nombrePages = 1
        else :
            nombrePages = int(lienDernierePage[0]['href'].split('page-')[1])

    with open('listeSymboles.txt', 'w') as file :
        for i in range(1, nombrePages + 1) :
            reponse = requests.get(baseUrl + str(i))
            if (reponse.ok) :
                soup = BeautifulSoup(reponse.text, 'lxml')
                lignesTableau = soup.findAll('tr', {'class' : 'c-table__row'})
                lignesTableau.pop(0)
                for ligne in lignesTableau :
                    symbole = ligne['data-ist']
                    nomAction = ligne.findAll('a')[0].text
                    reponse = requests.get('https://www.boursorama.com/_formulaire-periode/page-1?symbol=' + symbole)
                    soup = BeautifulSoup(reponse.text, 'lxml')
                    alerte = soup.findAll('p', {'class' : 'c-alert__text'})
                    if (len(alerte) == 0) :
                        file.write(nomAction + ';' + symbole + '\n')


# Récupération des valeurs historiques d'une action pour une période donnée
def CreerValeursHistoriques(actionSymbole, dateDepart, duree) :
    baseUrl = 'https://www.boursorama.com/_formulaire-periode/page-'
    complementUrl = '?symbol=' + actionSymbole + '&historic_search[startDate]=' + dateDepart + '&historic_search[duration]=' + duree + '&historic_search[period]=1'
    nombrePages = 0

    reponse = requests.get(baseUrl + "1" + complementUrl)
    if (reponse.ok) :
        soup = BeautifulSoup(reponse.text, 'lxml')
        lienDernierePage = soup.findAll('a', {'aria-label' : 'Dernière page'})
        if (len(lienDernierePage) == 0) :
            nombrePages = len(soup.findAll('a'))
        else :
            nombrePages = int(lienDernierePage[0]['href'].split('page-')[1].split('?symbol')[0])
        
    nomFichier = os.getcwd() + '\\data\\' + actionSymbole + '\\' + dateDepart.replace("/", "-") + '_' + duree + '.txt'

    if (os.path.exists(os.getcwd() + '\\data\\' + actionSymbole) == False) :
        os.mkdir(os.getcwd() + '\\data\\' + actionSymbole)

    with open(nomFichier, 'w') as file :
        for i in range(1, nombrePages + 1) :
            reponse = requests.get(baseUrl + str(i) + complementUrl)
            if (reponse.ok) :
                soup = BeautifulSoup(reponse.text, 'lxml')
                lignesTableau = soup.findAll('tr', {'class' : 'c-table__row'})
                for ligne in lignesTableau :
                    colonnes = ligne.findAll('td')
                    date = colonnes[0].text.strip()
                    ouverture = colonnes[5].text.strip()
                    cloture = colonnes[1].text.strip()
                    file.write(date + ';' + ouverture + ';' + cloture + '\n')


def CreerDonneesSimulation() :
    with open('listeSymboles.txt', 'r') as file :
        lines = file.readlines()
        for line in lines :
            symbole = line.strip().split(';')[1]
            CreerValeursHistoriques(symbole, '01/01/2019', '2Y')


CreerDonneesSimulation()
