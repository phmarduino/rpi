/*
  Sketch : pm_hass_v2_free_lolin-13042020.ino
  Description : Home Assistant, capteurs salon
                Mesure pression atmospherique, temperature, hygrometrie et luminosite
                Avec des capteurs BME280 et BH1750
  Création : PHMARDUINO le 13 avril 2020
  Mise a jour : ...
*/

//Include des Library
#include <ESP8266WiFi.h>    // Connexion WIFI
#include <PubSubClient.h>   // Publication MQTT de Nick O'Leary 
#include "SparkFunBME280.h" // Gestion capteur BME280 de SparkFun
#include <BH1750.h>         // Gestion capteur BH1750 de Christopher laws 

// Infos WIFI a adapter
const char* ssid = "freeboxLM";
const char* password = "722AB93D9F";

//Infos MQTT a adapter
const char* mqttServer = "192.168.0.8";  //Adresse IP du Broker MQTT
const int mqttPort = 1883;               //Port utilisé par le Broker MQTT

// Creation d un objet client WIFI
WiFiClient monClientWifi;
// Creation d un objet client publication MQTT s appuyant sur le client WIFI
PubSubClient monClientMqtt(monClientWifi);

//Creation d un objet monBme280 de type capteur BME280
BME280 monBme280;

//Creation d un objet lightMeter de type BH1750
BH1750 lightMeter;

void setup() {
  // Initialisation liaison serie
  Serial.begin(9600);

  // Affichage infos sketch
  Serial.println("pm_hass_v2_free_lolin-13042020");

   //Initialisation donnees du capteur BME280
  monBme280.settings.commInterface = I2C_MODE;
  monBme280.settings.I2CAddress = 0x76;

  //Configuration du capteur BME280
  monBme280.settings.runMode = 3;         // Mode normal, le capteur passe en mode sleep entre deux mesures
  monBme280.settings.tStandby = 0;        // 0.5 ms entre deux mesures
  monBme280.settings.filter = 0;          // Filter off, pas de filtrage en cas de variation brusque
  monBme280.settings.tempOverSample = 1;  // Suréchantillonnage x 1 cad resolution de 0.0050°C (16 bits)
  monBme280.settings.pressOverSample = 1; // Suréchantillonnage x 1 cad Résolution de 2.62 Pa (16 bits)
  monBme280.settings.humidOverSample = 1; // Suréchantillonnage x 1
  
  delay(10);  //Delai attente demarrage capteur, le BME280 demande 2 ms mini pour démarrer
              //Ici delai de 10 ms
  
  Serial.print("ID du capteur BME 280 : ");
  Serial.println(monBme280.begin(), HEX); // Chargement configuration BME280

   // Demarrage BH1750
  lightMeter.begin();
  
  // Connexion au WIFI
  Serial.print("Connexion en cours au reseau WIFI :  ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("Connexion au WIFI ok ... Adress IP locale du NodeMCU Lolin ");
  Serial.println(WiFi.localIP());

  // Init client MQTT pour la publication
  monClientMqtt.setServer(mqttServer, mqttPort);
}

void loop() {
  // Mesure temperature, pression et hygrometrie
  float h = monBme280.readFloatHumidity();        // Recup hygrometrie
  float t = monBme280.readTempC();                // Recup temperature
  float p = monBme280.readFloatPressure()/100;    // Recup pression atmo

   // Mesure luminosite    
  uint16_t lux = lightMeter.readLightLevel();
  Serial.print("Luminosite : ");
  Serial.print(lux);
  Serial.println(" lx");

  // Connexion au serveur MQTT
  while (!monClientMqtt.connected()) {
    Serial.println("Connexion au serveur MQTT ...");
    if (monClientMqtt.connect("53salonlolin")) {
      Serial.println("MQTT connecte");
    }
    else {
      Serial.print("Echec connexion serveur MQTT, code erreur= ");
      Serial.println(monClientMqtt.state());
      Serial.println("nouvel essai dans 2s");
    delay(2000);
    }
  }
  
  // Publication MQTT
    monClientMqtt.publish("home_53/salon/temp", String(t).c_str());
    monClientMqtt.publish("home_53/salon/humi", String(h).c_str());
    monClientMqtt.publish("home_53/salon/pres", String(p).c_str());
    monClientMqtt.publish("home_53/salon/lumi", String(lux).c_str());
  // Attente 1 mn avant de re publier
     delay(60000);

}
