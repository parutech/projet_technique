#TRI DES ENTREPRISES DANS LES CATEGORIE SUIVANTES : PME, ETI, GE 

import requests
import re
import os
from bs4 import BeautifulSoup

# 2019 

PME = []
ETI = []
GE = []
PME2 = []
ETI2 = []
GE2 = []
PME3 = []
ETI3 = []
GE3 = []
symb= []
ent = []
entreprises = []
Ca = []
effectif = []
bilan = []
Ca2 = []
effectif2 = []
bilan2 = []
Ca3 = []
effectif3 = []
bilan3 = []
dette = []
ebitda = []
PERs = []
PEG = []
listTuple = []
secteurs = []
PERClass1 = []
PERClass2 = []
PERClass3 = []
PERClass4 = []
PEGClass1 = []
PEGClass2 = []
compteur = 0
Evolutions = []

coeffPer = 4 
coeffPeg = 3 
coeffEvol  = 2
coeffTaille = 1

notes = [33,66,100]


notesEntreprise = []

notePers = []
notePegs = []

TaillesNote = []


def Taille2019():
    
### PER #########

    PME = []
    ETI = []
    GE = []
    symb= []
    ent = []
    entreprises = []
    Ca = []
    effectif = []
    bilan = []
    dette = []
    ebitda = []
    PERs = []
    PEG = []
    listTuple = []
    secteurs = []
    PERClass1 = []
    PERClass2 = []
    PERClass3 = []
    PERClass4 = []
    PEGClass1 = []
    PEGClass2 = []
    compteur = 0
    
    Taille1 = []
    Taille2 = []
    Taille3 = []

    with open('ListeSymboles.txt','r') as file: 
        f = file.readlines()
        for line in f:
            nomEntreprise=line.split(';')[0] 
            symbole = line.split(';')[1].split('\n')
            secteur = line.split(';')[2].split('\n')[0]
            entreprises.append(nomEntreprise)
            secteurs.append(secteur)

            try :
                with open(os.getcwd() + '\\data\\'+symbole[0]+'\\bilan.txt','r',encoding="latin-1") as file1:
                    f1 = file1.readlines()
                    ChiffAff = re.split("[;]",f1[0])
                    Ca.append(ChiffAff[1])
                    totalActif = re.split("[;]",f1[7])
                    bilan.append(totalActif[1])
                    Eff = re.split("[;]",f1[8])
                    effectif.append(Eff[1])
                                    
            except FileNotFoundError:
                print("Oops! pas de fichier pour le symbole",symbole[0])
                   
    # DEBUT DU TRI
    for z in zip(entreprises,Ca,effectif,bilan,secteurs):
        listTuple.append(z)
     
        nom = z[0]
        chiff = int(z[1].replace(" ",""))
        eff = int(z[2].replace(" ",""))
        bi = int(z[3].replace(" ",""))
        sect = z[4]
        if (chiff < 50000 or bi < 43000 )  and (eff<250):
            # print(nom+" est une PME du secteur",sect)
            PME.append(nom)
            Taille1.append("PME")
            
        elif (eff<5000 and eff>250) and ((chiff < 1500000 and chiff>50000) or (bi < 2000000 and bi > 43000)) : 
            # print(nom+" est une ETI du secteur",sect)
            ETI.append(nom)
            Taille1.append("ETI")
            
        else: 
            # print(nom+" "+" est une GE du secteur",sect)
            GE.append(nom)
            Taille1.append("GE")
            
    return Taille1
    
def NotePer():    
    with open('ListeSymboles.txt', 'r') as file: #permet de lire le fichier depuis le repertoire donné
        f = file.readlines()
        #Extraction du nom des entreprises
        for line in f:
            nomEntreprise=line.split(';')[0]
            symbole =line.split(';')[1].split('\n')
            secteur =line.split(';')[2].split('\n')[0]
            entreprises.append(nomEntreprise)
            secteurs.append(secteur)
            # print(entreprises)
            
                        
            with open(os.getcwd() + '\\data\\'+symbole[0]+'\\estimations.txt','r') as file2:
                f2 = file2.readlines()
                ebitdas = re.split("[;]",f2[0])
                ebitda.append(ebitdas[1])
                per = re.split("[;]",f2[1])
                PERs.append(per[1])
                dettes = re.split("[;]",f2[3])
                dette.append(dettes[1])  
                notePers = []
                notePegs = []
                for z in zip(entreprises,PERs):
                    
                    listTuple.append(z)
                    # print(listTuple)
                
                    nom = z[0]
                    indPer = float(z[1].replace(" ",""))    
                
                    #Vert 
                    if (indPer > 0 and indPer < 10) :
                        # print(nom+" : prix sous évalué",indPer)
                        PERClass1.append(nom)
                        notePer = notes[2]*coeffPer
                        notesEntreprise.append(notePer)
                        notePers.append(notePer)
                        
                    #Vert 
                    elif (indPer > 10 and indPer < 17) : 
                        # print(nom+" :  prix bon",indPer)
                        PERClass2.append(nom)
                        notePer = notes[2]*coeffPer
                        notePers.append(notePer)
                    #Orange     
                    elif (indPer > 17 and indPer < 25) : 
                        # print(nom+" : prix est surévalué ou s'attendre à de futurs bénéfices",indPer)
                        PERClass3.append(nom)
                        notePer = notes[1]*coeffPer
                        notePers.append(notePer)
                    #Orange   
                    else  : 
                        # print(nom+" : bulle spéculative ou très forts profits",indPer)
                        PERClass4.append(nom)
                        notePer = notes[1]*coeffPer
                        notePers.append(notePer)
        return notePers

### PEG #########

def NotePEG():
    for z in zip(entreprises,dette, ebitda):
        listTuple.append(z)
        nom = z[0]
        df = float(z[1].replace(" ",""))
        eb = float(z[2].replace(" ","")) 
        if (df != 0 and eb != 0):
            peg = df/eb
            PEG.append(peg)

          #VERT
            if (peg > 0 and peg <= 3) :
                #print(nom+" : situation correcte quant au remboursement de ses crédits",peg)
                PEGClass1.append(nom)
                notePeg = notes[2]*coeffPeg
                notePegs.append(notePeg)
                
        #Orange
                
            elif (peg > 3 and peg < 5) : 
                #print(nom+" : bof bof ",peg)
                PEGClass2.append(nom)
                notePeg = notes[1]*coeffPeg
                notePegs.append(notePeg)
                #Rouge
            elif (peg ==0) : 
                print("ZERRRRRROOO")
                # PEGClass2.append(nom)
                # notePeg = notes[1]*coeffPeg
                # notePegs.append(notePeg)
                #Rouge
            elif (peg < 0) : 
                notePeg = notes[2]*coeffPeg
                notePegs.append(notePeg)
            else :
                notePeg = notes[0]*coeffPeg
                notePegs.append(notePeg)
            
        else:
            
            notePeg = 50*coeffPeg #Medium dapres Diéééé chales
            notePegs.append(notePeg)
            PEG.append(0)
    return notePegs
            
#print(len(notePegs))    
        



    
#TRAITEMENT POUR UNE DEMANDE SPECIFIQUE 
#def RechercheEntreprise():
#    c = 0
#
#    demande = input("Quel Entreprise recherchez vous ?")
#
#    for e in listTuple:
#        
#    
#        if demande.lower() ==e[0].lower():
#            print(e)
#            c+=1
#    if (c==0):
#        
#           
#        print("Aucune entreprise trouvée")
        
        
   
    
        
#Création de la fonction générant la liste de tuple (Entreprise,Secteur)


#def ListeEntreprisesSecteurs(): 
#    ListEntrepriseSecteurs = []
#                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
#    
#    for y in zip(entreprises,secteurs):
#        ListEntrepriseSecteurs.append(y)
#    print(ListEntrepriseSecteurs)

    
    
#ListeEntreprisesSecteurs()
def RecupérationEntreprise():
    
    entreprises = []
  
   

    with open('ListeSymboles.txt','r') as file: 
        f = file.readlines()
        # print(len(f))
        for line in f:
            nomEntreprise=line.split(';')[0] 
            symbole =line.split(';')[1].split('\n')
            secteur =line.split(';')[2].split('\n')[0]
            entreprises.append(nomEntreprise)
    return entreprises  

def Taille2020():
    
    PME = []
    ETI = []
    GE = []
    symb= []
    ent = []
    entreprises = []
    Ca = []
    effectif = []
    bilan = []
    dette = []
    ebitda = []
    PERs = []
    PEG = []
    listTuple = []
    secteurs = []
    PERClass1 = []
    PERClass2 = []
    PERClass3 = []
    PERClass4 = []
    PEGClass1 = []
    PEGClass2 = []
    compteur = 0
    
    Taille1 = []
    Taille2 = []
    Taille3 = []

    with open('ListeSymboles.txt','r') as file: 
        f = file.readlines()
        # print(len(f))
        for line in f:
            
            nomEntreprise=line.split(';')[0] 
           
            symbole =line.split(';')[1].split('\n')
            secteur =line.split(';')[2].split('\n')[0]
           
            
            entreprises.append(nomEntreprise)
            secteurs.append(secteur)
               
            try :
                                
                with open(os.getcwd() + '\\data\\'+symbole[0]+'\\bilan.txt','r',encoding="latin-1") as file1:
                    f1 = file1.readlines()
                    ChiffAff = re.split("[;]",f1[0])
                    Ca.append(ChiffAff[2])
                    totalActif = re.split("[;]",f1[7])
                    bilan.append(totalActif[2])
                    Eff = re.split("[;]",f1[8])
                    effectif.append(Eff[2])
                                                
            except FileNotFoundError:
                print("Oops! pas de fichier pour le symbole",symbole[0])
                
      
    # DEBUT DU TRI
    for z in zip(entreprises,Ca,effectif,bilan,secteurs):
        listTuple.append(z)
        # print(listTuple)
        nom = z[0]
        chiff = int(z[1].replace(" ",""))
       
        eff = int(z[2].replace(" ",""))
            
        eff = int(z[2].replace(" ",""))
        # print(nom,eff,"ss")
        bi = int(z[3].replace(" ",""))
        sect = z[4]
        
        if (chiff < 50000 or bi < 43000 )  and (eff<250) :
            # print(nom+" est une PME du secteur",sect)
            PME.append(nom)
            Taille2.append("PME")
            noteTaille = notes[0]*coeffTaille
            TaillesNote.append(noteTaille)
            
        elif (eff<5000 and eff>250) and ((chiff < 1500000 and chiff>50000) or (bi < 2000000 and bi >43000)) : 
            # print(nom+" est une ETI du secteur",sect)
            ETI.append(nom)
            Taille2.append("ETI")
            noteTaille = notes[1]*coeffTaille
            TaillesNote.append(noteTaille)
            
        else: 
            # print(nom+" "+" est une GE du secteur",sect)
            GE.append(nom)
            Taille2.append("GE")
            noteTaille = notes[2]*coeffTaille
            TaillesNote.append(noteTaille)
    return Taille2
        


def Taille2021():
    
    PME = []
    ETI = []
    GE = []
    NonRepertorie = []
    symb= []
    ent = []
    entreprises = []
    Ca = []
    effectif = []
    bilan = []
    dette = []
    ebitda = []
    PERs = []
    PEG = []
    listTuple = []
    secteurs = []
    PERClass1 = []
    PERClass2 = []
    PERClass3 = []
    PERClass4 = []
    PEGClass1 = []
    PEGClass2 = []
    compteur = 0
    
    Taille1 = []
    Taille2 = []
    Taille3 = []

    with open('ListeSymboles.txt','r') as file: 
        f = file.readlines()
        #print(len(f))
        for line in f:
            
            nomEntreprise=line.split(';')[0] 
           
            symbole =line.split(';')[1].split('\n')
            secteur =line.split(';')[2].split('\n')[0]
           
            
            entreprises.append(nomEntreprise)
            secteurs.append(secteur)

            try :
                                
                with open(os.getcwd() + '\\data\\'+symbole[0]+'\\bilan.txt','r',encoding="latin-1") as file1:
                    f1 = file1.readlines()
                   
                    ChiffAff = re.split("[;]",f1[0])
                    Ca.append(ChiffAff[3])
                    
                    totalActif = re.split("[;]",f1[7])
                    
                    if totalActif[3] == '\n':
                        bilan.append(totalActif[2])
                    else:
                        bilan.append(totalActif[3])

                    Eff = re.split("[;]",f1[8])
                    if Eff[3] == '\n':
                        effectif.append(Eff[2])
                    else:
                        effectif.append(Eff[3])
                                                
            except FileNotFoundError:
                print("Oops! pas de fichier pour le symbole",symbole[0])
                
                     
    # DEBUT DU TRI
    for z in zip(entreprises,Ca,effectif,bilan,secteurs):
        listTuple.append(z)
        # print(listTuple)
        nom = z[0]
        chiff = int(z[1].replace(" ",""))
       
        eff = int(z[2].replace(" ",""))
        
        if eff == '\n':  
            eff = int(z[2].replace(" ",""))
            
        # print(nom,eff,"ss")
        bi = int(z[3].replace(" ",""))
        sect = z[4]
        compteur = 0
        
        if (chiff < 50000 or bi < 43000 )  and (eff<250) :
            # print(nom+" est une PME du secteur",sect)
            PME.append(nom)
            Taille3.append("PME")
            noteTaille = notes[0]*coeffTaille
            TaillesNote.append(noteTaille)
            compteur +=1 
        elif (eff<2500 and eff>250) and ((chiff < 1500000 and chiff>50000) or (bi < 2000000 and bi >43000)) : 
            # print(nom+" est une ETI du secteur",sect)
            ETI.append(nom)
            Taille3.append("ETI")
            noteTaille = notes[1]*coeffTaille
            TaillesNote.append(noteTaille)
            compteur +=1
        else:
            # print(nom+" "+" est une GE du secteur",sect)
            GE.append(nom)
            Taille3.append("GE")
            noteTaille = notes[2]*coeffTaille
            TaillesNote.append(noteTaille)
            
    return Taille3


def TailleNote():
    
    PME = []
    ETI = []
    GE = []
    NonRepertorie = []
    symb= []
    ent = []
    entreprises = []
    Ca = []
    effectif = []
    bilan = []
    dette = []
    ebitda = []
    PERs = []
    PEG = []
    listTuple = []
    secteurs = []
    PERClass1 = []
    PERClass2 = []
    PERClass3 = []
    PERClass4 = []
    PEGClass1 = []
    PEGClass2 = []
    compteur = 0
    
    Taille1 = []
    Taille2 = []
    Taille3 = []

    with open('ListeSymboles.txt','r') as file: 
        f = file.readlines()
        #print(len(f))
        for line in f:
            
            nomEntreprise=line.split(';')[0] 
           
            symbole =line.split(';')[1].split('\n')
            secteur =line.split(';')[2].split('\n')[0]
           
            
            entreprises.append(nomEntreprise)
            secteurs.append(secteur)
           
            try :
                                
                with open(os.getcwd() + '\\data\\'+symbole[0]+'\\bilan.txt','r',encoding="latin-1") as file1:
                    f1 = file1.readlines()
                    
                   
                    ChiffAff = re.split("[;]",f1[0])
                    Ca.append(ChiffAff[3])
                    
                    totalActif = re.split("[;]",f1[7])
                    
                    if totalActif[3] == '\n':
                       
                        
                        bilan.append(totalActif[2])
                    else:
                    
                        bilan.append(totalActif[3])
                    
                    Eff = re.split("[;]",f1[8])
                    if Eff[3] == '\n':
                        
                        effectif.append(Eff[2])
                    else:
                        
                        effectif.append(Eff[3])
                                         
            except FileNotFoundError:
                print("Oops! pas de fichier pour le symbole",symbole[0])     
    
                    
    # DEBUT DU TRI
    for z in zip(entreprises,Ca,effectif,bilan,secteurs):
        listTuple.append(z)
        # print(listTuple)
        nom = z[0]
        chiff = int(z[1].replace(" ",""))
        eff = int(z[2].replace(" ",""))
        
        if eff == '\n': 
            eff = int(z[2].replace(" ",""))

        # print(nom,eff,"ss")
        bi = int(z[3].replace(" ",""))
        sect = z[4]
        compteur = 0
        
        if (chiff < 50000 or bi < 43000 )  and (eff<250) :
            # print(nom+" est une PME du secteur",sect)
            PME.append(nom)
            Taille3.append("PME")
            noteTaille = notes[0]*coeffTaille
            TaillesNote.append(noteTaille)
            compteur +=1
        elif (eff<2500 and eff>250) and ((chiff < 1500000 and chiff>50000) or (bi < 2000000 and bi >43000)) : 
            # print(nom+" est une ETI du secteur",sect)
            ETI.append(nom)
            Taille3.append("ETI")
            noteTaille = notes[1]*coeffTaille
            TaillesNote.append(noteTaille)
            compteur +=1
        else:
            # print(nom+" "+" est une GE du secteur",sect)
            GE.append(nom)
            Taille3.append("GE")
            noteTaille = notes[2]*coeffTaille
            TaillesNote.append(noteTaille)
            
    return TaillesNote

cas = []

def NoteEvolution():
    for x in zip(Taille2019(),Taille2020(),Taille2021()):
        
        evolu = []
        evolu.append(x)
        cas.append(x)

        # print(x)
        # print(evolu)
        with open('TailleEntreprises.txt','a') as file4:
            file4.write(x[0]+" ")
            
            file4.write(x[1]+" ")
            
            file4.write(x[2])

            # file4.write(" "+x[3])
           
            file4.write("\n")
            #VERT
            
            #print(evolu[0])
            if  (evolu[0] == ('PME', 'PME', 'PME')):
                #print("STABLE")
                noteEvolu = notes[2]*coeffEvol
                Evolutions.append(noteEvolu)
            elif  (evolu[0] == ('GE', 'GE', 'GE')):
                #print("STABLE")
                noteEvolu = notes[2]*coeffEvol
                Evolutions.append(noteEvolu)
            elif  (evolu[0] == ('ETI', 'ETI', 'ETI')):
                #print("STABLE")
                noteEvolu = notes[2]*coeffEvol
                Evolutions.append(noteEvolu)
            elif  (evolu[0] == ('GE', 'ETI', 'GE')):
                #print("STABLE") 
                noteEvolu = notes[2]*coeffEvol
                Evolutions.append(noteEvolu)
            elif  (evolu[0] == ('GE', 'ETI', 'ETI')):
                #print("STABLE")
                noteEvolu = notes[2]*coeffEvol
                Evolutions.append(noteEvolu)
            elif  (evolu[0] == ('PME', 'GE', 'GE')):
                #print("STABLE")
                noteEvolu = notes[2]*coeffEvol
                Evolutions.append(noteEvolu)
            
                #VERT
            # CROISSANT
            
            
            elif  (evolu[0] == ('PME', 'PME', 'ETI')):
               #print("Croissant")
               noteEvolu = notes[2]*coeffEvol
               Evolutions.append(noteEvolu)
            elif  (evolu[0] == ('PME', 'ETI', 'ETI')):
                #print("Croissant")
                noteEvolu = notes[2]*coeffEvol
                Evolutions.append(noteEvolu)
            elif  (evolu[0] == ('PME', 'PME', 'GE')):
               #print("Croissant")
               noteEvolu = notes[2]*coeffEvol
               Evolutions.append(noteEvolu)
            elif  (evolu[0] == ('PME', 'ETI', 'GE')):
               #print("Croissant")
               noteEvolu = notes[2]*coeffEvol
               Evolutions.append(noteEvolu)
            elif  (evolu[0] == ('ETI', 'ETI', 'GE')):
               #print("Croissant")
               noteEvolu = notes[2]*coeffEvol
               Evolutions.append(noteEvolu)
            else:
                noteEvolu = notes[0]*coeffEvol
                Evolutions.append(noteEvolu)
                #print("Decroissant")
    return Evolutions


MoyenneEntreprise = []


def Moyenne():
    for i in zip(NotePer(),NotePEG(),NoteEvolution(),TailleNote()):
       m = (i[0] + i[1] + i[2] + i[3]) /10
       MoyenneEntreprise.append(m)
    return MoyenneEntreprise


def FonctionNote(entreprise):
    for i in zip(entreprises,Moyenne()):
        if (entreprise.upper() == i[0]):
            #print("Trouvé")
            return i[1]
       

print(FonctionNote("airbus"))