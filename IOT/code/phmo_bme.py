# Script de test du BME280 avec un RPI 2
# Pour la mesure de la temperature, de la pression atmospherique et du taux d'humidite
# Nom script : phmo_bme.py
# Date : 24 11 2017
# Source : https://github.com/rm-hull/bme280

#Initialisations
import smbus2
import bme280 

port = 1
address = 0x76
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus, address)

# Lecture des mesures
mesures = bme280.sample(bus, address)

# Affichage des mesures
print "Temps : ", (mesures.timestamp)
print "Temperature : ", (mesures.temperature), " Degre C"
print "Pression : ", (mesures.pressure), " hPa"
print "Humidite : ", (mesures.humidity), "%"



