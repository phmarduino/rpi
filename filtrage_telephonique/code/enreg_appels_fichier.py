#!/usr/local/bin/python
# coding: latin-1


# Nom script  : enreg_appels_fichier.py
# Description : Enregistrement des appels telephoniques dans un fichier
# Création    : phmarduino le 05 03 2020
# Mise à jour : phmarduino le 07 03 2020, ajout flush pour forcer ecriture fichier
# Mise à jour : phmarduino le 10 03 2020, ajout message informatifs
# Mise à jour :

import serial
import time

#Ouverture du fichier litse des appels en mode Append pour ajouter à la fin
Print ("Ouvertude du fichire des appels liste_appels.txt en append ...")
monfic = open("liste_appels.txt", "a")

#Initialisation objet mon_modem
Print ("Initialisaiton modem sur /dev/ttyACM0")
mon_modem = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=1)

Print("lancement de la boucle infinie d'ecoute du modem")
while 1:
    modem_infos = mon_modem.readline()
    if modem_infos != "":
        print modem_infos
        if ("DATE" in modem_infos):
            date_appel = (modem_infos[5:]).strip(' \t\n\r')
        if ("TIME" in modem_infos):
            heure_appel = (modem_infos[5:]).strip(' \t\n\r')
        if ("NMBR" in modem_infos):
            numero_appel = (modem_infos[5:]).strip(' \t\n\r')
            ma_ligne = "Nouvel appel le " + date_appel + ' a '+ heure_appel + ' du numero ' + numero_appel + '\n'
            print (ma_ligne) 
            print ("Ecriture nouvel enregistrement appel dans le fichier")
            monfic.write(ma_ligne)
            #Force le vidage buffer pour ecrire immediatement dans le fichier
            monfic.flush()

