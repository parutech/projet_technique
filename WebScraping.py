import os
import requests
from bs4 import BeautifulSoup

symbolesIncomplets = ['1rPAIR', '1rPAM', '1rPGNE', '1rPJCQ']

secteurs = {
    '0' : 'Pétrole et gaz',
    '1' : 'Matériaux de base',
    '2' : 'Industries',
    '3' : 'Biens de consommation',
    '4' : 'Santé',
    '5' : 'Services aux consommateurs',
    '6' : 'Télécommunications',
    '7' : 'Services aux collectivités',
    '8' : 'Sociétés financières',
    '9' : 'Technologies',
    '1rPAIR' : 'Aviation',
    '1rPAM' : 'Aviation',
    '1rPGNE' : 'Energie',
    '1rPJCQ' : 'Matériaux de base'
}

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
                        reponse = requests.get('https://www.boursorama.com/cours/' + symbole)
                        soup = BeautifulSoup(reponse.text, 'lxml')
                        if symbole in symbolesIncomplets :
                            secteur = secteurs[symbole]
                            print(nomAction + ';' + symbole + ';' + secteurs[symbole])
                            file.write(nomAction + ';' + symbole + ';' + secteurs[symbole] + '\n')
                        else :
                            lienSecteurList = soup.findAll('a', {'class' : 'c-link c-list-info__value c-link--animated'})
                            if (len(lienSecteurList) != 0) :
                                numeroSecteurList = lienSecteurList[0]['href'].split('industry%5D=')
                                if (len(numeroSecteurList) == 2) :
                                    numeroSecteur = numeroSecteurList[1].split('&filter')[0]
                                    print(nomAction + ';' + symbole + ';' + secteurs[str(numeroSecteur)])
                                    file.write(nomAction + ';' + symbole + ';' + secteurs[str(numeroSecteur)] + '\n')


# Récupération des valeurs historiques d'une action pour une période donnée
def CreerValeursHistoriques(actionSymbole, dateDepart, duree, param='w') :
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

    with open(nomFichier, param) as file :
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


# Récupération des données pour la simulation (2019-2021)
def CreerDonneesSimulation() :
    with open('listeSymboles.txt', 'r') as file :
        lines = file.readlines()
        for line in lines :
            symbole = line.strip().split(';')[1]
            if (os.path.exists(os.getcwd() + '\\data\\' + symbole + '\\01-01-2019_2Y.txt') == False) :
                CreerValeursHistoriques(symbole, '01/01/2019', '2Y')


# Récupération des données pour la simulation (2016-2019)
def CreerDonneesHistoriques() :
    with open('listeSymboles.txt', 'r') as file :
        lines = file.readlines()
        for line in lines :
            symbole = line.strip().split(';')[1]
            if (os.path.exists(os.getcwd() + '\\data\\' + symbole + '\\01-01-2016_3Y.txt') == False) :
                CreerValeursHistoriques(symbole, '01/01/2016', '3Y')


# Récupération des données de bilan d'entreprise
def CreerDonneesBilan() :
    with open('listeSymboles.txt', 'r') as file :
        lines = file.readlines()
        for line in lines :
            symbole = line.strip().split(';')[1]
            hreftxt = os.getcwd() + '\\data\\' + symbole + '\\' + 'bilan.txt'

            newurl = (
            'https://www.boursorama.com/cours/societe/chiffres-cles/' + symbole + '/')

            newresponse = requests.get(newurl)
            soup2 = BeautifulSoup(newresponse.text, 'lxml')
            lignesTableau = soup2.findAll('tr', {'class': 'c-table__row'})

            with open(hreftxt, 'a') as file:
                for ligne in lignesTableau:
                    nombres = ligne.findAll('div')
                    for nombre in nombres:
                        (nombre.text.strip())
                        file.write(nombre.text.strip() + ';')
                    file.write('\n')

            with open(hreftxt, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if 'Trésorerie' in line:
                        treso = line
                    if "Chiffre d'affaires de l'année" in line:
                        ca = line
                    if 'Résultat net' in line:
                        resunet = line
                    if 'Résultat opérationnel' in line:
                        resuope = line
                    if 'Résultat net part du groupe dilué par action' in line:
                        resunetact = line
                    if 'Rentabilité financière' in line:
                        rentafinance = line
                    if "Ratio d'endettement" in line:
                        ratiod = line
                    if 'Total actif' in line:
                        totalactif = line
                    if "Effectif en fin d'année" in line :
                        effectif = line

            with open (hreftxt,'w') as file:
                file.write(ca)
                file.write(treso)
                file.write(resunet)
                file.write(resuope)
                file.write(resunetact)
                file.write(rentafinance)
                file.write(ratiod)
                file.write(totalactif)
                file.write(effectif)