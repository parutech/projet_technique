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

dateActuelle
listeObjetsActions
listeActionsSelect
listeBoutonsSelect = []

portefeuille = Portefeuille(500000)

def init() :
    pass

if (__name__ == '__main__') :
    filePath = os.getcwd() + '\\ListeSymboles.txt'
    if (os.path.exists(filePath) == False) :
        init()

#-----------------------------------------------------------------#





#boutons graphique action
def db1():
    tk.Button.destroy(b1)
    tk.Button.destroy(b1destroy)

def db2():
    tk.Button.destroy(b2)
    tk.Button.destroy(b2destroy)
    
def db3():
    tk.Button.destroy(b3)
    tk.Button.destroy(b3destroy)
    
def db4():
    tk.Button.destroy(b4)
    tk.Button.destroy(b4destroy)
    
def db5():
    tk.Button.destroy(b5)
    tk.Button.destroy(b5destroy)
    
def db6():
    tk.Button.destroy(b6)
    tk.Button.destroy(b6destroy)
    

def selected(evt):
    global X
    global b1
    global b1destroy
    global b2
    global b2destroy
    global b3
    global b3destroy
    global b4
    global b4destroy
    global b5
    global b5destroy
    global b6
    global b6destroy
    
    value=(liste.get(ACTIVE))
    print(X)
    print(value)
   
    X = np.append(X, value)
    print(len(X))
    if len(X)==2:
        b1 = tk.Button(window, text =X[1], command = action1)
        b1.place(x=70, y=80)
        b1destroy = tk.Button(window, text ="X",command = db1)
        b1destroy.place(x=50, y=80)
    if len(X)==3:
        b2 = tk.Button(window, text =X[2])
        b2.place(x=70, y=110)
        b2destroy = tk.Button(window, text ="X",command = db2)
        b2destroy.place(x=50, y=110)
    if len(X)==4:
        b3 = tk.Button(window, text =X[3])
        b3.place(x=70, y=140)
        b3destroy = tk.Button(window, text ="X",command = db3)
        b3destroy.place(x=50, y=140)
    if len(X)==5:
        b4 = tk.Button(window, text =X[4])
        b4.place(x=70, y=170)
        b4destroy = tk.Button(window, text ="X",command = db4)
        b4destroy.place(x=50, y=170)
    if len(X)==6:
        b5 = tk.Button(window, text =X[5])
        b5.place(x=70, y=200)
        b5destroy = tk.Button(window, text ="X",command = db5)
        b5destroy.place(x=50, y=200)
    if len(X)==7:
        b6 = tk.Button(window, text =X[7])
        b6.place(x=70, y=230)
        b6destroy = tk.Button(window, text ="X",command = db6)
        b6destroy.place(x=50, y=230)
    if len(X)>7:
        X = np.array("t")
        tk.Button.destroy(b1)
        tk.Button.destroy(b1destroy)
        
        tk.Button.destroy(b2)
        tk.Button.destroy(b2destroy)
        
        tk.Button.destroy(b3)
        tk.Button.destroy(b3destroy)
        
        tk.Button.destroy(b4)
        tk.Button.destroy(b4destroy)
        
        tk.Button.destroy(b5)
        tk.Button.destroy(b5destroy)
        
        tk.Button.destroy(b6)
        tk.Button.destroy(b6destroy)






#graphique
def graphique(nom, duree):
    for action in listeActionsSelect:
        if action.getNom() == nom:
            dates, donnes = action.getDonneesGraphiques(duree)
            
    fig, ax = plt.subplots(1, 1, constrained_layout=True, figsize=(5, 5))
    
    ax.plot(dates, donnes)
    for label in ax.get_xticklabels():
        label.set_rotation(40)
        label.set_horizontalalignment('right')
    ax.set_title(nom)
    graphique = FigureCanvasTkAgg(fig, master = window)   
    graphique.draw()
    graphique.get_tk_widget().place(x=550, y=60)
    toolbar = NavigationToolbar2Tk(graphique,window) 
    toolbar.update()
    graphique.get_tk_widget().place(x=550, y=60)


#fenetre
window = tk.Tk()
window.title("MyWallet")
frame = tk.Frame(master=window, width=1500, height=1000)
frame.pack()


#recherche action
def callbackFunc():
    entry = entryString.get().upper()
    with open("ListeSymboles.txt",'r') as file:
        lines = file.readlines()
        N = len(lines)
        Z=np.array("f")
        for line in lines:
            if entry in line:
                d = re.split("[;]",line)
                Z=np.append(Z, d[0])
    
    for i in range(len(Z)-1):
        liste.insert(i, Z[1+i])
    
    liste.place(x=200, y=70)
    liste.bind('<<ListboxSelect>>',selected)

X = np.array("t")

liste = tk.Listbox(window,selectmode='extended')

entryString = tk.StringVar()
entry = tk.Entry(window, width=20, textvariable=entryString)
entry.place(x=200, y=50)

resultButton = tk.Button(window, text = 'Get Result',command=callbackFunc)
resultButton.place(x=327, y= 50)



#titre de section#*

img = ImageTk.PhotoImage(Image.open("image-3.jpg"))
background = tk.Label(master=frame, image = img)
background.place(x=0, y=0)


label1 = tk.Label(master=frame, text="Recherhe une action",  font=("Agency FB",17),fg='black', bg = '#A4D3E8')
label1.place(x=70, y=10)

label2 = tk.Label(master=frame, text="Actions en cours",  font=("Agency FB",17),fg='black', bg = '#A4D3E8')
label2.place(x=550, y=10)

label3 = tk.Label(master=frame, text="Mon portefeuille",  font=("Agency FB",17),fg='black', bg = '#A4D3E8')
label3.place(x=70, y=505)


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
label6.place(x=1000, y=450)

def etallonage(nombre):
    xe1 = int((nombre*2.7) +1000)
    ye1 = 450

    if (nombre<=33):
        NomEtalon = "Risqué"
    elif(nombre>33) & (nombre<66):
        NomEtalon = "Risque Moyen"
    else:
        NomEtalon = "Risque Leger"

    img3 = ImageTk.PhotoImage(Image.open("curseur.jpg"))
    label5 = tk.Label(master=frame, image = img3, highlightthickness=0)
    label5.place(x=xe1, y=ye1)

    label7 = tk.Label(master=frame, text=NomEtalon,  font=("Agency FB",15),fg='black', bg = '#A4D3E8')
    label7.place(x=1100, y=400)

etallonage(66)

#bouton graphique
def week():
    global duree
    duree = "2W"
    graphique()
def month():
    global duree
    time = "2M"
    graphique()
def year():
    global duree
    duree = "1Y"
    graphique()
    
groupe = tk.StringVar()
bouton1 = tk.Radiobutton(window,text='2 semaines',variable=groupe, value='s', command= week)
bouton2 = tk.Radiobutton(window,text='2 mois    ',variable=groupe, value='m', command= month)
bouton3 = tk.Radiobutton(window,text='1 ans     ',variable=groupe, value='a', command= year)
bouton1.place(x=560, y=470)
bouton2.place(x=660, y=470)
bouton3.place(x=760, y=470)

#popup nombre d'action a acheter ou vendre

def fenetreAchat():
    #fenetre
    popupa = tk.Tk()
    popupa.geometry('400x300')
    popupa.title('Achats')
    popupa.config(background= '#A4D3E8')
    #label acheter l'action de ...
    nomAction= "l'Oréal"
    text = "Acheter des actions de" + nomAction
    labelpop = tk.Label(popupa, text= text,  font=("Agency FB",15),fg='black', bg = '#A4D3E8')
    labelpop.place(x=100, y=4)
    #prix unitaire de l'action
    prix= "9"
    text2= "Prix unitaire de l'action :" + prix + "$"
    labelpop2 = tk.Label(popupa, text= text2,  font=("Agency FB",15),fg='black', bg = '#A4D3E8')
    labelpop2.place(x=100, y=40)
    #barre de recherche et bouton ok
    entryInt = tk.IntVar()
    entre = tk.Entry(popupa, width=10, textvariable=entryInt)
    entre.place(x=130,y=100)
    btnok = tk.Button(popupa, text='OK', command= lambda : popupAchat(entre))
    btnok.place(x=200,y=100)
    # Fonds restants et popup
def popupAchat(entre):
    liquidite= 200
    nbrSaisi = entre.get()
    prix = 9
    if (nbrSaisi.isnumeric()) :
        nbrSaisi = int(nbrSaisi)
        fond = liquidite - nbrSaisi * prix
        if fond > 0 :
            fond = str(fond)
            tk.messagebox.showinfo(" ", "Accepté : il vous reste" + fond + "$")
            #print(fond)
            #print(nbrSaisi)
        else : 
            tk.messagebox.showerror("Erreur", "Il n'y a pas assez de fonds")
    else :
        tk.messagebox.showerror("Erreur", "Saisir des chiffres")
            
            
     
    
def fenetreVente():
    #fenetre
    popup = tk.Tk()
    popup.geometry('400x300')
    popup.title('Vente')
    popup.config(background= '#A4D3E8')
    #label acheter l'action de ...
    nomAction= "l'Oréal"
    text = "Vendre des actions de" + nomAction
    labelpop = tk.Label(popup, text= text,  font=("Agency FB",15),fg='black', bg = '#A4D3E8')
    labelpop.place(x=100, y=4)
    #prix unitaire de l'action
    prix= "9"
    text2= "Prix unitaire de l'action :" + prix + "$"
    labelpop2 = tk.Label(popup, text= text2,  font=("Agency FB",15),fg='black', bg = '#A4D3E8')
    labelpop2.place(x=100, y=40)
    #barre de recherche et bouton ok
    entryInt = tk.IntVar()
    entre = tk.Entry(popup, width=10, textvariable=entryInt)
    entre.place(x=130,y=100)
    btnok = Button(popup, text='OK',command= lambda : popupVente(entre))
    btnok.place(x=200,y=100)
#Fonf restant et popup
def popupVente(entre):
    liquidite= 200
    nbrSaisi = entre.get()
    if (nbrSaisi.isnumeric()) :
        nbrSaisi = int(nbrSaisi)
        fond = liquidite - nbrSaisi
        if fond > 0 :
            print(fond)
            print(nbrSaisi)
        else : 
            tk.messagebox.showerror("Erreur", "Il n'y a pas assez d'action")
    else :
        tk.messagebox.showerror("Erreur", "Saisir des chiffres")
        
        
        
btnachat = Button(window, text="Acheter", command = fenetreAchat)
btnachat.place(x= 1200, y=40)    


btnachat = Button(window, text="Vendre", command = fenetreVente)
btnachat.place(x= 1200, y=90)    
    

def thing():
    my_label.config(text='1 jour avant')

def thing1():
    my1_label.config(text='1 jour apres')

def thing2():
    my2_label.config(text='2 jours apres')


##creation du bouton 1 jour avant
precedent_btn = PhotoImage(file='left1.png')
img_label = Label(image=precedent_btn)
#button
my_button= Button(window,image=precedent_btn,command=thing,borderwidth=0)
my_button.place(x=300,y=510)
#label
# my_label=Label(window,text='')
# my_label.place(x=30,y=10)


##creation du bouton 1 jour apres
suivant_btn = PhotoImage(file='right1.png')
img_label = Label(image=suivant_btn)
#Button
my1_button= Button(window,image=suivant_btn,command=thing1,borderwidth=0)
my1_button.place(x=333,y=510)
#label
# my1_label=Label(window,text='')
# my1_label.place(x=50,y=10)


##creation du bouton 2 jours apres 
suivant1_btn = PhotoImage(file='suivant1.png')
img2_label = Label(image=suivant1_btn)
#Button
my2_button= Button(window,image=suivant1_btn,command=thing2,borderwidth=0)
my2_button.place(x=366,y=510)
#label 
# my2_label=Label(window,text='')
# my2_label.place(x=70,y=10)

window.mainloop()