#!/usr/local/bin/python
# coding: latin-1

# Nom script  : test_modem_at.py
# Description : Test des commandes AT pour un modem 56 k
# Création    : phmarduino le 04 03 2020
# Mise à jour :

import serial
import time

# Initialisation fichier
monfic = open("monfic_modem.txt", "w")
monfic.write("Informations sur le modem")

#Initialisation objet modem
modem = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=1)

#Suppression echo
modem.write(str.encode('ATE0\r'))

#Activation presentation du numero appelant
#Faire un test avec numero masque

#Recup code produit modem
modem.write(str.encode('ATI0\r'))
cdprodbrut=modem.read(100)
cdprod=cdprodbrut[8:12]
print ("Code produit modem : ",cdprod)
malig = "\nCode produit modem : " + cdprod
monfic.write(malig)

#Recup version du firmware
modem.write(str.encode('ATI3\r'))
verfirmbrut=modem.read(100)
verfirm=verfirmbrut[2:35]
print ("Version firmware modem : ",verfirm)
malig = "\nVersion firmware modem : " + verfirm
monfic.write(malig)

#Demande dernier numero de telephone compose par le modem
modem.write(str.encode('ATDL?\r'))
dernutelbrut=modem.read(100)
dernutel=dernutelbrut[2:11]
print ("Dernier numero compose : ",dernutel)
malig = "\nDernier numero compose : " + dernutel
monfic.write(malig)

monfic.write("\n")



