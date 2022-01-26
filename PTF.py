from contextlib import closing
import datetime
import os
from django.forms import SelectDateWidget
import pandas

import WebScraping
import AnalyseStrategique
import AnalyseTechnique

dateActuelle = datetime.date(2019, 1, 1)
listeObjetsActions = []
listeActionsSelect = []

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
                    self.derniereValeur = self.getValeur()
                    # print(nom, symbole, secteur)
                    listeObjetsActions.append(self)

    def setQuantite(self, quantite) :
        self.quantite = quantite

    def getQuantite(self) :
        return self.quantite

    def getNom(self) :
        return self.nom

    def setDonneesSimulation(self) : 
        filePath = os.getcwd() + '\\data\\' + self.symbole + '\\01-01-2019_2Y.txt'
        if (os.path.exists(filePath) == False) :
            WebScraping.CreerValeursHistoriques(self.symbole, '01/01/2019', '2Y')

    def setDonneesGraphiques(self) : 
        filePath = os.getcwd() + '\\data\\' + self.symbole + '\\01-01-2018_3Y.txt'
        if (os.path.exists(filePath) == False) :
            WebScraping.CreerValeursHistoriques(self.symbole, '01/01/2018', '3Y')

    def setDonneesHistoriques(self) :
        dateHistorique = dateActuelle
        dateHistorique = datetime.date((dateActuelle.year - 3), dateActuelle.month, dateActuelle.day)
        strDateHistorique = dateHistorique.strftime('%d/%m/%Y')
        filePath = os.getcwd() + '\\data\\' + self.symbole + '\\' + strDateHistorique.replace('/', '-') + '_3Y.txt'
        if (os.path.exists(filePath) == False) :
            WebScraping.CreerValeursHistoriques(self.symbole, strDateHistorique, '3Y')

    def getDonneesGraphiques(self, duree = '2W') :
        self.setDonneesGraphiques()
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
        return AnalyseStrategique.FonctionNote(self.getNom())

    def getParametresOptimaux(self) :
        self.setDonneesHistoriques()
        dateHistorique = dateActuelle
        dateHistorique.year = dateActuelle.year - 3
        strDateHistorique = dateHistorique.strftime('%d/%m/%Y')
        return AnalyseTechnique.AnalyserValeursHistoriques(self.symbole, strDateHistorique)

    def getPosition(self) :
        shortPeriod, longPeriod, hysteresis = self.getParametresOptimaux()
        cheminFichier = os.getcwd() + '\\data\\' + self.symbole + '\\01-01-2018_3Y.txt'
        dataFrame = pandas.read_csv(cheminFichier, sep=';', names=['Date', 'Ouverture', 'Cloture'])[::-1]
        strDateActuelle = dateActuelle.strftime('%d/%m/%Y')
        indexJourActuel = dataFrame.index[dataFrame['Date'] == strDateActuelle]
        closingData = dataFrame['Ouverture'].tolist()[:(indexJourActuel + 1)]
        listEMAshort = AnalyseTechnique.CalculerEMA(closingData, shortPeriod)
        listEMAlong = AnalyseTechnique.CalculerEMA(closingData, longPeriod)
        return AnalyseTechnique.CalculerPositions(listEMAshort, listEMAlong, hysteresis)[-1]

class Portefeuille :
    global dateActuelle

    def __init__(self, liquidite, listeActions = []) -> None:
        self.listeActions = listeActions
        self.liquidite = liquidite

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

    def acheterAction(self, action, quantite) :
        prixTotal = action.getValeur() * quantite
        if (prixTotal <= self.liquidite) :
            if (action.getQuantite == 0) :
                self.listeActions.append(action)
            action.setQuantite(action.getQuantite() + quantite)
            self.setLiquidite(self.getLiquidite() - prixTotal)
            return self.liquidite
        else :
            return -1

    def vendreAction(self, action, quantite) :
        prixTotal = action.getValeur() * quantite
        if (quantite <= action.getQuantite()) :
            action.setQuantite(action.getQuantite() - quantite)
            self.setLiquidite(self.getLiquidite() + prixTotal)
            if (action.getQuantite == 0) :
                self.listeActions.remove(action)
            return self.liquidite
        else :
            return -1