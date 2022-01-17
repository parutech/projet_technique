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
    '1rPAIR' : 'Industries',
    '1rPAM' : 'Technologies',
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

    with open('ListeSymboles.txt', 'w', encoding='utf8') as file :
        for i in range(1, nombrePages + 1) :
            reponse = requests.get(baseUrl + str(i))
            if (reponse.ok) :
                soup = BeautifulSoup(reponse.text, 'lxml')
                lignesTableau = soup.findAll('tr', {'class' : 'c-table__row'})
                lignesTableau.pop(0)
                for ligne in lignesTableau :
                    symbole = ligne['data-ist']
                    nomAction = ligne.findAll('a')[0].text
                    reponse = requests.get('https://www.boursorama.com/_formulaire-periode/page-1?symbol=' + symbole + '&historic_search[startDate]=01/01/2016&historic_search[duration]=1M&historic_search[period]=1')
                    soup = BeautifulSoup(reponse.text, 'lxml')
                    alerte = soup.findAll('p', {'class' : 'c-alert__text'})
                    if (len(alerte) == 0) :
                        reponse = requests.get('https://www.boursorama.com/cours/' + symbole)
                        soup = BeautifulSoup(reponse.text, 'lxml')
                        if symbole in symbolesIncomplets :
                            secteur = secteurs[symbole]
                            file.write(nomAction + ';' + symbole + ';' + secteurs[symbole] + '\n')
                        else :
                            lienSecteurListe = soup.findAll('a', {'class' : 'c-link c-list-info__value c-link--animated'})
                            if (len(lienSecteurListe) != 0) :
                                numeroSecteurListe = lienSecteurListe[0]['href'].split('industry%5D=')
                                if (len(numeroSecteurListe) == 2) :
                                    numeroSecteur = numeroSecteurListe[1].split('&filter')[0]
                                    file.write(nomAction + ';' + symbole + ';' + secteurs[str(numeroSecteur)] + '\n')


# Récupération des valeurs historiques d'une action pour une période donnée
def CreerValeursHistoriques(symbole, dateDepart, duree, param='w') :
    baseUrl = 'https://www.boursorama.com/_formulaire-periode/page-'
    complementUrl = '?symbol=' + symbole + '&historic_search[startDate]=' + dateDepart + '&historic_search[duration]=' + duree + '&historic_search[period]=1'
    nombrePages = 0

    reponse = requests.get(baseUrl + "1" + complementUrl)
    if (reponse.ok) :
        soup = BeautifulSoup(reponse.text, 'lxml')
        lienDernierePage = soup.findAll('a', {'aria-label' : 'Dernière page'})
        if (len(lienDernierePage) == 0) :
            nombrePages = len(soup.findAll('a'))
        else :
            nombrePages = int(lienDernierePage[0]['href'].split('page-')[1].split('?symbol')[0])
        
    nomFichier = os.getcwd() + '\\data\\' + symbole + '\\' + dateDepart.replace('/', '-') + '_' + duree + '.txt'

    if (os.path.exists(os.getcwd() + '\\data\\' + symbole) == False) :
        os.mkdir(os.getcwd() + '\\data\\' + symbole)

    with open(nomFichier, param) as file :
        for i in range(1, nombrePages + 1) :
            reponse = requests.get(baseUrl + str(i) + complementUrl)
            if (reponse.ok) :
                soup = BeautifulSoup(reponse.text, 'lxml')
                lignesTableau = soup.findAll('tr', {'class' : 'c-table__row'})
                for ligne in lignesTableau :
                    colonnes = ligne.findAll('td')
                    date = colonnes[0].text.strip().replace(' ', '')
                    ouverture = colonnes[5].text.strip().replace(' ', '')
                    cloture = colonnes[1].text.strip().replace(' ', '')
                    file.write(date + ';' + ouverture + ';' + cloture + '\n')


# Récupération des données de bilan d'entreprise
def CreerDonneesBilan() :
    with open('ListeSymboles.txt', 'r') as file :
        lines = file.readlines()
        for line in lines :
            symbole = line.strip().split(';')[1]
            bilantxt = os.getcwd() + '\\data\\' + symbole + '\\' + 'bilan.txt'

            url = ('https://www.boursorama.com/cours/societe/chiffres-cles/' + symbole + '/')

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            lignesTableau = soup.findAll('tr', {'class': 'c-table__row'})

            with open(bilantxt, 'a') as file:
                for ligne in lignesTableau:
                    nombres = ligne.findAll('div')
                    for nombre in nombres:
                        (nombre.text.strip())
                        file.write(nombre.text.strip() + ';')
                    file.write('\n')

            with open(bilantxt, 'r') as file:
                lines = file.readlines()
                for line in lines :
                    if 'Trésorerie' in line :
                        treso = line
                    if "Chiffre d'affaires de l'année" in line :
                        ca = line
                    if 'Résultat net' in line :
                        resunet = line
                    if 'Résultat opérationnel' in line :
                        resuope = line
                    if 'Résultat net part du groupe dilué par action' in line :
                        resunetact = line
                    if 'Rentabilité financière' in line :
                        rentafinance = line
                    if "Ratio d'endettement" in line :
                        ratiod = line
                    if 'Total actif' in line :
                        totalactif = line
                    if "Effectif en fin d'année" in line :
                        effectif = line

            with open (bilantxt, 'w', encoding='utf8') as file:
                file.write(ca)
                file.write(treso)
                file.write(resunet)
                file.write(resuope)
                file.write(resunetact)
                file.write(rentafinance)
                file.write(ratiod)
                file.write(totalactif)
                file.write(effectif)


# Récupérer les données d'estimation de l'entreprise
def CreerDonneesEstimation() :
    with open('ListeSymboles.txt', 'r') as file :
        lines = file.readlines()
        for line in lines :
            symbole = line.strip().split(';')[1]
            estimationstxt = os.getcwd() + '\\data\\' + symbole + '\\' + 'estimations.txt'

            url = ('https://www.boursorama.com/cours/consensus/' + symbole + '/')

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            lignesTableau = soup.findAll('tr', {'class': 'c-table__row c-table-evolution__row-top'})

            with open(estimationstxt, 'a') as file:
                for ligne in lignesTableau:
                    nombres = ligne.findAll('td')
                    for nombre in nombres:
                        nombrestr = str(nombre)
                        nombrestr = nombrestr.split('>')[1].split('<')[0].strip()
                        file.write(nombrestr + ';')
                    file.write('\n')

            with open(estimationstxt, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if 'EBITDA' in line:
                        ebitda = line
                    if 'PER' in line:
                        per = line
                    if 'Bénéfice net par action' in line:
                        benef = line
                    if 'Dette financière nette' in line :
                        dettefin = line

            with open (estimationstxt, 'w', encoding='utf8') as file:
                file.write(ebitda)
                file.write(per)
                file.write(benef)
                file.write(dettefin)