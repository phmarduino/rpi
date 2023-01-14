#!/usr/local/bin/python
# coding: utf8

# Nom script  : serveur_tel.py
# Description : Gestion liste blanche
# Création    : phmarduino le 14 03 2020
# Mise à jour : phmarduino le 15/10/2020 changement port par defaut 5000 
# Mise à jour :

import sqlite3 as sql
import datetime
from flask import Flask, render_template, request, flash


# Application WEB Flask filtrage telephonique

# Creation de l application
app = Flask(__name__)

#Page d accueil
@app.route('/')
def index():
    now = datetime.datetime.now()
    madate = now.strftime("%d-%m-%Y")
    monheure = now.strftime("%H:%M")
    con = sql.connect("/home/pi/modem_appels/gestion_tel.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    # recup nombre de contacts stockés en table
    cur.execute("select count(*) from phm_liste_blanche")
    rows0 = cur.fetchall()
    # recup nombre d'appels stockés en table
    cur.execute("select count(*) from phm_appels")
    rows1 = cur.fetchall()
    # recup du dernier appel stockés en table
    cur.execute("select * from phm_appels order by nu_appel desc limit 1")
    rows2 = cur.fetchall()
    templateData = {
        'madate' : madate,
        'monheure': monheure,
        'nbappels': rows1[0][0],
        'nbcontacts': rows0[0][0]
      }
    return render_template('index.html', rows2=rows2, **templateData)

#Page liste des appels    
@app.route('/liste')
def liste_appels():
    con = sql.connect("/home/pi/modem_appels/gestion_tel.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from phm_appels")
    rows = cur.fetchall()
    return render_template("liste_appels.html",rows = rows)
    
#Page liste des contacts    
@app.route('/liste_contacts')
def liste_contacts():
    con = sql.connect("/home/pi/modem_appels/gestion_tel.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from phm_liste_blanche")
    rows = cur.fetchall()
    return render_template("affic_liste_blanche.html",rows = rows)   
    
#Page Informations contact liste blanche    
@app.route('/contact')
def contact():
    return render_template("contact.html")      

@app.route('/addcontact',methods = ['POST', 'GET'])
def addcontact():
    now = datetime.datetime.now()
    madate = now.strftime("%d-%m-%Y")
    monheure = now.strftime("%H:%M:%S")
    nb_appels=0
    if request.method == 'POST':
        try:
            nom = request.form['nom']
            num_tel = request.form['numtel']
            typec = request.form['typec']
            indicatif = request.form['indicatif']
            
            with sql.connect("/home/pi/modem_appels/gestion_tel.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO phm_liste_blanche (nom,type,indicatif,num_tel,date_ajout,heure_ajout,nb_appels)VALUES (?,?,?,?,?,?,?)",(nom,typec,indicatif,num_tel,madate,monheure,nb_appels) )
                con.commit()
                msg = "Creation contact reussie"
        except:
            con.rollback()
            msg = "Erreur creation contact"
            
        finally:
            return render_template("resultsqlite.html",msg = msg)
            con.close()
            
@app.route('/delete_contact', methods=['POST'])
def delete_contact():
    con = sql.connect("/home/pi/modem_appels/gestion_tel.db")
    cur = con.cursor()
    cur.execute('DELETE FROM phm_liste_blanche WHERE num_tel=?',[request.form['num_tel_del']])
    con.commit()
    msg = "Suppression contact effectuee"
    return render_template("resultsqlite.html",msg = msg)
    con.close()
   
#Port par défaut 5000 à modifier par le bon port  !!!!!!!!!!!          
#Port par défaut 5000 à modifier par le bon port  !!!!!!!!!!!
#Port par défaut 5000 à modifier par le bon port  !!!!!!!!!!!
#cf tableau excel des ports
app.run(debug=True, host='0.0.0.0', port=5000)




