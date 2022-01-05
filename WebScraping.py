import requests
from bs4 import BeautifulSoup


# Récupération de la liste de toutes les actions présentes sur Euronext Paris
def ListeSymboles() :
    baseUrl = 'https://www.boursorama.com/bourse/actions/cotations/page-'
    nombrePages = 0

    reponse = requests.get(baseUrl + "1")
    if (reponse.ok) :
        soup = BeautifulSoup(reponse.text, 'lxml')
        lienDernierePage = soup.find_all('a', {'aria-label' : 'Dernière page'})
        if (len(lienDernierePage) == 0) :
            nombrePages = 1
        else :
            nombrePages = int(lienDernierePage[0]['href'].split('page-')[1])

    with open('listeSymboles.txt', 'w') as file :
        file.write('Action;Symbole' + '\n')
        for i in range(1, nombrePages + 1) :
            reponse = requests.get(baseUrl + str(i))
            if (reponse.ok) :
                soup = BeautifulSoup(reponse.text, 'lxml')
                lignesTableau = soup.find_all('tr', {'class' : 'c-table__row'})
                lignesTableau.pop(0)
                for ligne in lignesTableau :
                    symbole = ligne['data-ist']
                    nomAction = ligne.find_all('a')[0].text
                    print(nomAction + ';' + symbole)
                    file.write(nomAction + ';' + symbole + '\n')

    
# Récupération des valeurs historiques d'une action pour une période donnée
def ValeursHistoriques(actionSymbole, dateDepart, duree) :
    baseUrl = 'https://www.boursorama.com/_formulaire-periode/page-'
    complementUrl = '?symbol=' + actionSymbole + '&historic_search[startDate]=' + dateDepart + '&historic_search[duration]=' + duree + '&historic_search[period]=1'
    nombrePages = 0

    reponse = requests.get(baseUrl + "1" + complementUrl)
    if (reponse.ok) :
        soup = BeautifulSoup(reponse.text, 'lxml')
        lienDernierePage = soup.find_all('a', {'aria-label' : 'Dernière page'})
        if (len(lienDernierePage) == 0) :
            nombrePages = len(soup.find_all('a'))
        else :
            nombrePages = int(lienDernierePage[0]['href'].split('page-')[1].split('?symbol')[0])
        
    nomFichier = actionSymbole + '_' + dateDepart.replace("/", "-") + '_' + duree + '.txt'

    with open(nomFichier, 'w') as file :
        file.write('Date;Ouverture;Cloture' + '\n')
        for i in range(1, nombrePages + 1) :
            reponse = requests.get(baseUrl + str(i) + complementUrl)
            if (reponse.ok) :
                soup = BeautifulSoup(reponse.text, 'lxml')
                lignesTableau = soup.find_all('tr', {'class' : 'c-table__row'})
                for ligne in lignesTableau :
                    colonnes = ligne.find_all('td')
                    date = colonnes[0].text.strip()
                    ouverture = colonnes[5].text.strip()
                    cloture = colonnes[1].text.strip()
                    print(date + ';' + ouverture + ';' + cloture)
                    file.write(date + ';' + ouverture + ';' + cloture + '\n')


#ListeSymboles()
ValeursHistoriques('1rPAF', '01/01/2020', '2M')

