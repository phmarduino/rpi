# Script : rpipme_one.py
# Description : Mesure temperature, humidite et pression avec un
#               BME280 sur un RPI avec stockage des mesures dans
#               InfluxDB pour visualiation ave Grafana
# Date        : 01/12/2017
# Auteur      : PHMO
# Sources     : Inspire de https://github.com/rm-hull/bme280

import time
from influxdb import InfluxDBClient
import smbus2
import bme280

port = 1
address = 0x76
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus, address)

# Parametres InfluxDB
host = "localhost"
port = 8086
user = "root"
password = "root"
dbname = "rpibme"

# Initialisation du client InfluxDB
client = InfluxDBClient(host, port, user, password, dbname)

# Prise de mesures
data = bme280.sample(bus, address)
# Affichage des mesures du bme280

# Enregistrement des mesures dans InfluxDB
json_body = [
{
    "measurement": "phm_mesures",
    "tags": {
        "lieu": "MLV",
        "capteur": "RPI-BME280"
    },
    "fields": {
        "temp": round(data.temperature,2),
        "humi": round (data.humidity,2),
        "press": round (data.pressure,2)
    }
}
]

client.write_points(json_body)
