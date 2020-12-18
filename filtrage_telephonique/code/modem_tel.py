#!/usr/local/bin/python
# coding: utf8

#############################################################
# Nom script  : modem_tel.py
# Description : Gestion appels telephoniques avec un modem 56K
# Création    : phmarduino le 13 03 2020, version initiale
# Mise à jour : phmarduino le 29 03 2020, ajout liste blanche
# Mise à jour : 
#############################################################

#############################################################
# Import de fonctions externes

import serial
import sqlite3 as sql
import datetime
import time

#############################################################
# Dénifition locale de fonctions

#Fonction de recherche num de tel sur le site doisjerepondre
#pour recuperer les opinions sur un num de tel non trouve en 
#liste blanche

def search_tel(num_tel):
	mon_url="https://www.doisjerepondre.fr/numero-de-telephone/" + num_tel
	r = requests.get(mon_url)
	print(r.status_code)
	chaine=r.content
	pos1 = chaine.find('x négative') 
	pos2 = chaine.find('x neutre') 
	print ("test pour : %s",mon_url)
	print ("pos1 : %s",pos1)
	print ("pos2 : %s",pos2)
	if pos1 == -1:
		print("pas d opinion negative trouvee")
		opi1=""
	else:
		deb=pos1-10
		fin=pos1+11
		opi=chaine[deb:fin]
		deb1=opi.find('>')+1
		opi1=opi[deb1:]
		print(opi1)
		
	if pos2 == -1:
		print("pas d opinion neutre trouvee")
		opi2=""
	else:
		deb=pos2-10
		fin=pos2+8
		opi=chaine[deb:fin]
		deb1=opi.find('>')+1
		opi2=opi[deb1:]
		print(opi2)
	return(opi1+" "+opi2)


#############################################################
# Corps principal de programme

#Initialisation objet modem
modem = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=1)

#Suppression echo
modem.write(str.encode('ATE0\r'))

#RAZ du modem
modem.write(str.encode('ATZ\r'))

#Activation presentation du numero appelant
modem.write(str.encode('AT#CID=1\r')) 

#Recup code produit modem
modem.write(str.encode('ATI0\r'))
modem_infos = modem.readlines()
print ("Retour modem : %s",modem_infos)
cdprod = modem_infos[7].strip() 
print("Code produit modem : ",cdprod)

#Recup version du firmware
modem.write(str.encode('ATI3\r'))
modem_infos = modem.readlines()
print ("Retour modem : %s",modem_infos)
verfirm = modem_infos[1].strip()  
print("Version firmware modem : ",verfirm)

print ("Lancement ecoute modem .......")

#############################################################
# Boucle d'attente infinie

while 1:
    modem_infos = modem.readline()
    # Traitement d un nouvel appel entrant
    if modem_infos != "":
        print modem_infos
        # Ligne de données modem de type date
        if ("DATE" in modem_infos):
            date_appel = (modem_infos[5:]).strip(' \t\n\r')
        # Ligne de données modem de type heure
        if ("TIME" in modem_infos):
            heure_appel = (modem_infos[5:]).strip(' \t\n\r')
        # Ligne de données modem de type numero de tel appelant
        if ("NMBR" in modem_infos):
            numero_appel = (modem_infos[5:]).strip(' \t\n\r')
            ma_ligne = "Nouvel appel le " + date_appel + ' a '+ heure_appel + ' du numero ' + numero_appel + '\n'
            print (ma_ligne) 
            
            # Recherche numero appelant en liste blanche
            print("Recherche numero appelant en liste blanche")
            con = sql.connect("/home/pi/modem_appels/gestion_tel.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM phm_liste_blanche WHERE num_tel = ?", (numero_appel,))
            data=cur.fetchone()
            
            # L'appelant est bien en liste blanche
            if data :
                print('Nom %s trouve avec le numero de tel %s dans la liste blanche'%(data[3],numero_appel))
                nom_appel=data[3]
                nb_appels=data[8]
                ind_rejet="non"	            
                print('Mise a jour de la liste blanche pour l appelant')
                now = datetime.datetime.now()
                madate = now.strftime("%d-%m-%Y")
                monheure = now.strftime("%H:%M:%S")
                nb_appels+=1
                monsql="""Update phm_liste_blanche set nb_appels=?, dat_der_app=?, heur_der_app=? WHERE num_tel = ?"""
                mesdata=(nb_appels,madate,monheure,numero_appel)
                cur.execute(monsql, mesdata)
                con.commit()   
                # Alimentation resultat recherche liste blanche  
                res="Present en liste blanche"
                print ("resultat : ")
                print (res)         
                
            # L'appelant n'est pas en liste blanche       
            else:
                print('Numero %s pas dans la liste blanche'%(numero_appel))
                nom_appel="***** INCONNU *****" 
                print("On demande au modem de decrocher")
                #modem.write(str.encode('ATH1\r'))
                print("On fait une pause de 2 seconde")
                time.sleep(2)               
                print ("On demande au modem de raccrocher")
                #modem.write(str.encode('ATH0\r'))
                print ("Recherche sur le site doisjerepondre infos sur l appelant")
                # Alimentation resultat recherche liste blanche
                res="Rejet : "+search_tel(numero_appel).decode('utf-8')
                print ("resultat : ")
                print (res)
                
 
            print("Enregistrement de l appel entrant en base")   
            now = datetime.datetime.now()
            madate = now.strftime("%d-%m-%Y")
            monheure = now.strftime("%H:%M:%S")
            con = sql.connect("/home/pi/modem_appels/gestion_tel.db")
            cur = con.cursor()
            cur.execute("INSERT INTO phm_appels (date_modem,heure_modem,num_tel,ind_rejet,nom_appel) VALUES (?,?,?,?,?)",(madate,monheure,numero_appel,res,nom_appel))
            con.commit()
            con.close()


