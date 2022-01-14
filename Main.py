# Fichier principal qui appellera les fichiers de scraping, d'analyse, et de rendu pour l'application

import WebScraping
#import AnalyseFondamentale
#import AnalyseTechnique
#import Application

#WebScraping.CreerListeSymboles()
WebScraping.CreerDonneesSimulation()
WebScraping.CreerDonneesHistoriques('01/01/2016')
WebScraping.CreerDonneesBilan()
WebScraping.CreerDonneesEstimation()

#Nom de l'action, secteur, ouverture, fermeture, historique (2sem, 2mois, 1an)

class Action :
    def __init__(self) -> None:
        pass

    pass


class Portefeuille :
    def __init__(self) -> None:
        pass

    pass