# Fichier principal qui appellera les fichiers de scraping, d'analyse, et de rendu pour l'application

import datetime
import os
import pandas

import WebScraping
# import AnalyseFondamentale
import AnalyseTechnique

# WebScraping.CreerListeSymboles()
# WebScraping.CreerDonneesSimulation()
# WebScraping.CreerDonneesAffichage()
# WebScraping.CreerDonneesHistoriques('01/01/2016')
# WebScraping.CreerDonneesBilan()
# WebScraping.CreerDonneesEstimation()

dateActuelle = datetime.date(2019, 1, 1)

# Nom de l'action, secteur, ouverture, fermeture, historique (2sem, 2mois, 1an)

""" dateDebut = datetime.date(2019, 1, 1)
dateFin = datetime.date(2021, 12, 31)

dateActuelle = datetime.date(2019, 1, 1)
jourActuel = dateActuelle.weekday()

strDateActuelle = dateActuelle.strftime('%d/%m/%Y')

print(dateActuelle, jourActuel, strDateActuelle) """


class Action :
    global dateActuelle

    def __init__(self, nom) -> None:
        with open('ListeSymboles.txt', 'r') as fichier :
            lignes = fichier.readlines()
            for ligne in lignes :
                if nom in ligne :
                    lineSplit = ligne.split(';')
                    self.nom = lineSplit[0]
                    self.symbole = lineSplit[1]
                    self.secteur = lineSplit[2]
                    self.quantite = 0

                    self.setDonneesSimulation()
                    self.setDonneesGraphiques()
                    self.setDonneesHistoriques()

                    self.valeur = self.getValeur()
                    self.derniereValeur = self.valeur
                    self.sentiment = self.getSentiment()
                    self.parametres = self.getParametresOptimaux()


    def setQuantite(self, quantite) :
        self.quantite = quantite


    def getQuantite(self) :
        return self.quantite


    def setDonneesSimulation(self) : 
        filePath = os.getcwd() + '\\data\\' + self.symbole + '\\01-01-2019_2Y.txt'
        if (os.path.exists(filePath) == False) :
            WebScraping.CreerValeursHistoriques(self.symbole, '01/01/2019', '2Y')
        pass


    def setDonneesGraphiques(self) : 
        filePath = os.getcwd() + '\\data\\' + self.symbole + '\\01-01-2018_3Y.txt'
        if (os.path.exists(filePath) == False) :
            WebScraping.CreerValeursHistoriques(self.symbole, '01/01/2018', '3Y')
        pass


    def setDonneesHistoriques(self) :
        dateHistorique = dateActuelle
        dateHistorique.year = dateActuelle.year - 3
        strDateHistorique = dateHistorique.strftime('%d/%m/%Y')
        filePath = os.getcwd() + '\\data\\' + self.symbole + '\\' + strDateHistorique.replace('/', '-') + '_3Y.txt'
        if (os.path.exists(filePath) == False) :
            WebScraping.CreerValeursHistoriques(self.symbole, strDateHistorique, '3Y')
        pass


    def getDonneesGraphiques(self, duree) :
        cheminFichier = os.getcwd() + '\\data\\' + self.symbole + '\\01-01-2018_3Y.txt'

        dates = []
        donnees = []

        if (duree == '2W') :
            dateDebut = dateActuelle - datetime.timedelta(14)
        elif (duree == '2M') :
            dateDebut = dateActuelle - datetime.timedelta(60)
        elif (duree == '1Y') :
            dateDebut = dateActuelle - datetime.timedelta(365)

        dataFrame = pandas.read_csv(cheminFichier, sep=';', names=['Date', 'Ouverture', 'Cloture'])[::-1]
        while (dateDebut != dateActuelle) :
            strDateDebut = dateDebut.strftime('%d/%m/%Y')
            for index in dataFrame.index:
                if (dataFrame['Date'][index] == strDateDebut) :
                    dates.append(dateDebut)
                    donnees.append(dataFrame['Ouverture'][index])
            dateDebut = dateDebut + datetime.timedelta(1)

        return [dates, donnees]


    def getValeur(self) :
        cheminFichier = os.getcwd() + '\\data\\' + self.symbole + '\\01-01-2019_2Y.txt'

        dataFrame = pandas.read_csv(cheminFichier, sep=';', names=['Date', 'Ouverture', 'Cloture'])[::-1]
        strDateActuelle = dateActuelle.strftime('%d/%m/%Y')
        indexJourActuel = dataFrame.index[dataFrame['Date'] == strDateActuelle]

        return dataFrame['Ouverture'][indexJourActuel]


    def getSentiment(self) :
        
        pass


    def getParametresOptimaux(self) :
        dateHistorique = dateActuelle
        dateHistorique.year = dateActuelle.year - 3
        strDateHistorique = dateHistorique.strftime('%d/%m/%Y')
        return AnalyseTechnique.AnalyserValeursHistoriques(self.symbole, strDateHistorique)


class Portefeuille :
    global dateActuelle


    def __init__(self) -> None:
        self.listeActions = []
        self.liquidite = 0


    def getValeur(self) :
        valeur = self.liquidite
        for action in self.listeActions :
            valeur = valeur + (action.getValeur() * action.getQuantite())
        return valeur


    def getLiquidite(self) :
        return self.liquidite


    def getListeActions(self) :
        return self.listeActions


    def setListeActions(self, listeActions) :
        self.listeActions = listeActions

    
    def setLiquidite(self, liquidite) :
        self.liquidite = liquidite

    
    def vendreAction(self, nom) :
        for action in self.listeActions :
            if (action.nom == nom) :
                self.liquidite = self.liquidite + action.getValeur()
                action.setQuantite(action.quantite - 1)
                if (action.getQuantite() == 0) :
                    self.getListeActions.remove(action)


    def acheterAction(self, nom) :
        for action in self.listeActions :

            pass