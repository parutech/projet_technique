# Fichier principal qui appellera les fichiers de scraping, d'analyse, et de rendu pour l'application

import WebScraping
#import AnalyseFondamentale
#import AnalyseTechnique
#import Application

WebScraping.CreerListeSymboles()
WebScraping.CreerDonneesSimulation()
WebScraping.CreerDonneesBilan()
WebScraping.CreerDonneesEstimation()