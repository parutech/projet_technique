# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 09:20:57 2022

@author: Laure
"""

import tkinter as tk
from tkinter import*
import datetime
import os
import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from tkinter.filedialog import *
from tkinter.messagebox import *
from PIL import ImageTk
from PIL import Image
from PTF import *
import datetime

d = 0
duree = '2W'

dateActuelle = datetime.date(2019, 1, 1)
listeDates = []
listeObjetsActions

listeDatesPtf
listeValeursPtf
listeLabelsPtf = []
labelLiquidite = None

actionSelectionnee = None

graphiquePortefeuille = None
graphiqueAction = None
labelCurseur = None


portefeuille = Portefeuille(500000)

#fenetre
window = tk.Tk()
window.title("MyWallet")
frame = tk.Frame(master=window, width=1500, height=1000)
frame.pack()

labelNom = tk.Label(master=window, text="Nom : ")
labelSecteur = tk.Label(master=window, text="Secteur : ")
labelPrix = tk.Label(master=window, text="Prix : -- €")
labelQuantite = tk.Label(master=window, text="Quantité : ")
labelSentiment = tk.Label(master=window, text="Sentiment : --/100")
btnachat = tk.Button(window, text="Acheter", command = None)
btnvente = tk.Button(window, text="Vendre", command = None)

labelNom.place(x= 50, y=100)
labelSecteur.place(x= 50, y=120)
labelPrix.place(x= 50, y=140)
labelQuantite.place(x= 50, y=160)
labelSentiment.place(x= 50, y=180)
btnachat.place(x= 1400, y=150)
btnvente.place(x= 1400, y=200)

def init() :
    WebScraping.CreerListeSymboles()


#-----------------------------------------------------------------#


def afficherLabelsAction(action) :
    global actionSelectionnee
    global labelNom 
    global labelSecteur 
    global labelPrix 
    global labelQuantite 
    global labelSentiment
    global btnachat
    global btnvente
    global duree

    actionSelectionnee = action
    labelNom.config(text="Nom : " + action.getNom())
    labelSecteur.config(text="Secteur : " + str(action.getSecteur()))
    labelPrix.config(text="Prix : " + str(action.getValeur(dateActuelle)) + "€")
    labelQuantite.config(text="Quantité : " + str(action.getQuantite()))
    labelSentiment.config(text="Sentiment : " + str(action.getSentiment()) + "/100")
    etallonage(action.getSentiment())

    btnachat.config(command = lambda : fenetreAchat(action))
    btnvente.config(command = lambda : fenetreVente(action))

    graphiqueActn(action, duree)

def selected(evt):
    value=(liste.get(ACTIVE))
    for action in listeObjetsActions:
        if action.getNom() == value :
            afficherLabelsAction(action)


#graphique action
def graphiqueActn(action, duree):
    global graphiqueAction   
    dates = []
    durees = []

    if graphiqueAction is not None :
        graphiqueAction.get_tk_widget().destroy()

    dates, donnes = action.getDonneesGraphiques(dateActuelle, duree)
    fig, ax = plt.subplots(1, 1, constrained_layout=True, figsize=(8, 3))
    ax.plot(dates, donnes)

    for label in ax.get_xticklabels():
        label.set_rotation(40)
        label.set_horizontalalignment('right')
    ax.set_title(action.getNom())
    graphiqueAction = FigureCanvasTkAgg(fig, master = window)   
    graphiqueAction.draw()
    graphiqueAction.get_tk_widget().place(x=550, y=90)
    toolbar = NavigationToolbar2Tk(graphiqueAction,window) 
    toolbar.update()


#graphique portefeuille
def graphiquePtf():
    global graphiquePortefeuille

    if graphiquePortefeuille is not None :
        graphiquePortefeuille.get_tk_widget().destroy()

    fig, ax = plt.subplots(1, 1, constrained_layout=True, figsize=(9, 4))
    ax.plot(listeDatesPtf, listeValeursPtf)

    for label in ax.get_xticklabels():
        label.set_rotation(40)
        label.set_horizontalalignment('right')
    ax.set_title('Valeur du portefeuille')
    graphiquePortefeuille = FigureCanvasTkAgg(fig, master = window)
    graphiquePortefeuille.draw()
    graphiquePortefeuille.get_tk_widget().place(x=500, y=550)
    toolbar = NavigationToolbar2Tk(graphiquePortefeuille,window) 
    toolbar.update()


#recherche action
def callbackFunc():
    liste.delete(0, END)
    listeEntries = []
    entry = entryString.get().upper()
    for action in listeObjetsActions :
        if entry in action.getNom() :
            listeEntries.append(action.getNom())

    #print(entry)
    #print(listeEntries)

    for i in range(len(listeEntries)) :
        liste.insert(i, listeEntries[i])
    
    liste.place(x=270, y=40)
    liste.bind('<<ListboxSelect>>',selected)

liste = tk.Listbox(window,selectmode='extended')

entryString = tk.StringVar()
entry = tk.Entry(window, width=20, textvariable=entryString)
entry.place(x=270, y=20)

resultButton = tk.Button(window, text = 'Get Result',command=callbackFunc)
resultButton.place(x=400, y= 20)


#titre de section#*
img = ImageTk.PhotoImage(Image.open("image-3.jpg"))
background = tk.Label(master=frame, image = img)
background.place(x=0, y=0)

label1 = tk.Label(master=frame, text="Rechercher une action",  font=("Agency FB",17),fg='black', bg = '#A4D3E8')
label1.place(x=70, y=10)

label2 = tk.Label(master=frame, text="Action sélectionnée",  font=("Agency FB",17),fg='black', bg = '#A4D3E8')
label2.place(x=550, y=10)

label3 = tk.Label(master=frame, text="Actions conseillées",  font=("Agency FB",17),fg='black', bg = '#A4D3E8')
label3.place(x=70, y=350)

label4 = tk.Label(master=frame, text="Mon portefeuille",  font=("Agency FB",17),fg='black', bg = '#A4D3E8')
label4.place(x=70, y=510)


#lignes
canv = tk.Canvas(window, width=2, height=500, bg="black",highlightthickness=0)
canv.place(x=500, y=3)
canv = tk.Canvas(window, width=850, height=2, bg="black",highlightthickness=0)
canv.place(x=500, y=501)
canv = tk.Canvas(window, width=850, height=2, bg="black",highlightthickness=0)
canv.place(x=0, y=501)


#curseur etalonnage
img2 = ImageTk.PhotoImage(Image.open("etalonnage.jpg"))
label6 = tk.Label(master=frame, image = img2, highlightthickness=0)
label6.place(x=1100, y=450)

def etallonage(nombre):
    global labelCurseur

    if labelCurseur is not None :
        tk.Label.destroy(labelCurseur)

    xe1 = int((nombre * 2.7) + 1100)
    ye1 = 450

    if (nombre<=33):
        NomEtalon = "Risqué"
    elif(nombre>33) & (nombre<66):
        NomEtalon = "Risque Moyen"
    else:
        NomEtalon = "Risque Leger"

    img3 = ImageTk.PhotoImage(Image.open("curseur.jpg"))
    labelCurseur = tk.Label(master=frame, image = img3, highlightthickness=0)
    labelCurseur.place(x=xe1, y=ye1)

    label7 = tk.Label(master=frame, text=NomEtalon,  font=("Agency FB",15),fg='black', bg = '#A4D3E8')
    label7.place(x=1200, y=400)


#bouton graphique
def week():
    global duree
    duree = "2W"
    graphiqueActn(actionSelectionnee, duree)
def month():
    global duree
    duree = "2M"
    graphiqueActn(actionSelectionnee, duree)
def year():
    global duree
    duree = "1Y"
    graphiqueActn(actionSelectionnee, duree)
    

groupe = tk.StringVar()
bouton1 = tk.Radiobutton(window,text='2 semaines',variable=groupe, value='s', command= week)
bouton2 = tk.Radiobutton(window,text='2 mois    ',variable=groupe, value='m', command= month)
bouton3 = tk.Radiobutton(window,text='1 an      ',variable=groupe, value='a', command= year)
bouton1.place(x=560, y=450)
bouton2.place(x=660, y=450)
bouton3.place(x=760, y=450)


#popup nombre d'action a acheter ou vendre
def fenetreAchat(action):
    #fenetre
    popupa = tk.Tk()
    popupa.geometry('400x300')
    popupa.title('Achats')
    popupa.config(background= '#A4D3E8')
    #label acheter l'action de ...
    nomAction= action.getNom()
    text = "Acheter des actions de " + nomAction
    labelpop = tk.Label(popupa, text= text,  font=("Agency FB",15),fg='black', bg = '#A4D3E8')
    labelpop.place(x=100, y=4)
    #prix unitaire de l'action
    prix= action.getValeur(dateActuelle)
    text2= "Prix unitaire de l'action : " + str(prix) + "€"
    labelpop2 = tk.Label(popupa, text= text2,  font=("Agency FB",13),fg='black', bg = '#A4D3E8')
    labelpop2.place(x=100, y=35)
    #liquidite dispo
    liq = portefeuille.getLiquidite()
    text3= "Liquidité disponible : " + str(liq) + "€ (Max = " + str(int(liq/prix)) + ")"
    labelpop3 = tk.Label(popupa, text= text3,  font=("Agency FB",13),fg='black', bg = '#A4D3E8')
    labelpop3.place(x=100, y=60)
    #barre de recherche et bouton ok
    entryInt = tk.IntVar()
    entre = tk.Entry(popupa, width=10, textvariable=entryInt)
    entre.place(x=130,y=100)
    btnok = tk.Button(popupa, text='OK', command= lambda : popupAchat(entre, action))
    btnok.place(x=200,y=100)
# Fonds restants et popup
def popupAchat(entre, action):
    nbrSaisi = entre.get()
    if (nbrSaisi.isnumeric()) :
        nbrSaisi = int(nbrSaisi)
        fonds = portefeuille.acheterAction(dateActuelle, action, nbrSaisi)
        if (fonds != -1) :
            tk.messagebox.showinfo(" ", "Accepté : il vous reste " + str(fonds) + "€")
            #print(portefeuille.getListeActions())
        else : 
            tk.messagebox.showerror("Erreur", "Il n'y a pas assez de fonds")
    else :
        tk.messagebox.showerror("Erreur", "Saisir des chiffres")
     
    
def fenetreVente(action):
    #fenetre
    popup = tk.Tk()
    popup.geometry('400x300')
    popup.title('Achats')
    popup.config(background= '#A4D3E8')
    #label acheter l'action de ...
    nomAction= action.getNom()
    text = "Acheter des actions de " + nomAction
    labelpop = tk.Label(popup, text= text,  font=("Agency FB",15),fg='black', bg = '#A4D3E8')
    labelpop.place(x=100, y=4)
    #prix unitaire de l'action
    prix= action.getValeur(dateActuelle)
    text2= "Prix unitaire de l'action : " + str(prix) + "€"
    labelpop2 = tk.Label(popup, text= text2,  font=("Agency FB",13),fg='black', bg = '#A4D3E8')
    labelpop2.place(x=100, y=35)
    #liquidite dispo
    liq = portefeuille.getLiquidite()
    text3= "Liquidité disponible : " + str(liq) + "€ (Max = " + str(action.getQuantite()) + ")"
    labelpop3 = tk.Label(popup, text= text3,  font=("Agency FB",13),fg='black', bg = '#A4D3E8')
    labelpop3.place(x=100, y=60)
    #barre de recherche et bouton ok
    entryInt = tk.IntVar()
    entre = tk.Entry(popup, width=10, textvariable=entryInt)
    entre.place(x=130,y=100)
    btnok = tk.Button(popup, text='OK', command= lambda : popupVente(entre, action))
    btnok.place(x=200,y=100)
#Fonf restant et popup
def popupVente(entre, action):
    nbrSaisi = entre.get()
    if (nbrSaisi.isnumeric()) :
        nbrSaisi = int(nbrSaisi)
        fonds = portefeuille.vendreAction(dateActuelle, action, nbrSaisi)
        if (fonds != -1) :
            tk.messagebox.showinfo(" ", "Accepté : il vous reste " + str(fonds) + "€")
            #print(portefeuille.getListeActions())
        else : 
            tk.messagebox.showerror("Erreur", "Il n'y a pas assez d'actions")
    else :
        tk.messagebox.showerror("Erreur", "Saisir des chiffres")


def afficherPtf():
    global labelLiquidite
    global listeLabelsPtf

    if labelLiquidite is not None :
        tk.Label.destroy(labelLiquidite)
    
    if listeLabelsPtf is not [] :
        for label in listeLabelsPtf :
            tk.Label.destroy(label)

    ycoord = 600
    xcoord = 70

    for action in portefeuille.getListeActions() :
        labelAction = tk.Label(master=window, text=str(action.getNom()) + ' (' + str(action.getPosition(dateActuelle)) + ')')
        labelAction.place(x=70, y=ycoord)
        listeLabelsPtf.append(labelAction)
        ycoord = ycoord + 20

    labelLiquidite = tk.Label(master=window, text='Liquidité : ' + str(portefeuille.getLiquidite()) + '€', font=("Agency FB",17))
    labelLiquidite.place(x=200, y=510)


def passer1(graph = 1):
    global d
    global dateActuelle
    global listeDatesPtf
    global listeValeursPtf
    global graphiquePortefeuille
    if (dateActuelle != listeDates[-1]) :
        listeDatesPtf.append(listeDates[d])
        listeValeursPtf.append(portefeuille.getValeur(dateActuelle))
        # print(listeDatesPtf)
        # print(listeValeursPtf)
        d = d + 1
        dateActuelle = listeDates[d]
        if graph :
            graphiquePtf()
            afficherPtf()

def passer30():
    for i in range(29) :
        passer1(0)
    passer1()


##creation du bouton 1 jour apres
suivant_btn = PhotoImage(file='right1.png')
img_label = Label(image=suivant_btn)
#Button
my1_button= Button(window,image=suivant_btn,command=passer1,borderwidth=0)
my1_button.place(x=950,y=510)


##creation du bouton 30 jours apres 
suivant1_btn = PhotoImage(file='suivant1.png')
img2_label = Label(image=suivant1_btn)
#Button
my2_button= Button(window,image=suivant1_btn,command=passer30,borderwidth=0)
my2_button.place(x=983,y=510)


if (__name__ == '__main__') :
    filePath = os.getcwd() + '\\ListeSymboles.txt'
    if (os.path.exists(filePath) == False) :
        init()
    
    with open((os.getcwd() + '\\ListeSymboles.txt'), 'r') as file :
        for line in file.readlines() :
            listeObjetsActions.append(Action(line.strip().split(';')[0], dateActuelle))

    cheminFichier = os.getcwd() + '\\data\\1rPAB\\01-01-2019_2Y.txt'
    dataFrame = pandas.read_csv(cheminFichier, sep=';', names=['Date', 'Ouverture', 'Cloture'])[::-1]
    listeDatesEx = dataFrame['Date'].tolist()
    
    for date in listeDatesEx :
        listeDates.append(datetime.datetime.strptime(date, '%d/%m/%Y').date())

    dateActuelle = listeDates[0]

    # print(listeDates)
    # print(listeObjetsActions)

    window.mainloop()