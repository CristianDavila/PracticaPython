# Cristian Davila Carmona
# Segon script

#!/usr/bin/python

import sys
import math
import csv
import urllib
import xml.etree.ElementTree as ET

#ordenar lista: sorted(list)


def distancia(lat1, long1, lat2, long2):
    radioTierra = 6371  #kilometros
    lat1 = (lat1*math.pi / 180)
    long1 = (long1*math.pi / 180)
    lat2 = (lat2*math.pi / 180)
    long2 = (long2*math.pi / 180)
    dist = radioTierra * math.acos(math.sin(lat1)*math.sin(lat2) + math.cos(lat1)*math.cos(lat2) * math.cos(long2-long1))
    return dist





if len(sys.argv) == 2:
        print "String:",sys.argv[1]
        palabra = sys.argv[1]
else:
    print "Parametros incorrectos!"
    sys.exit()



targets = []
estaciones = []
estacionesSlots = []
estacionesBikes = []

restaurantfile  = open('restaurants.csv', "rb")
restaurantreader = csv.reader(restaurantfile)
fileBicing = urllib.urlopen("http://wservice.viabicing.cat/getstations.php?v=1")



for row in restaurantreader:
        x = row[0].count(palabra)
        if x > 0:
            targets.append(row)


for row in targets:
        print row[0]


a = fileBicing.read()
root = ET.fromstring(a)

for child in root.iter('station'):
    if child.find('status').text == 'OPN':
        ident = child.find('id').text
        lat = child.find('lat').text
        lon = child.find('long').text
        slots = child.find('slots').text
        bikes = child.find('bikes').text

        estaciones.append([ident, lat, lon, slots, bikes, 0])

for restaurante in targets:
    for station in estaciones:
        distPunts = distancia(float(restaurante[2]), float(restaurante[3]), float(station[1]), float(station[2]))
        station[5] = distPunts
        if distPunts <= 1.0 and int(station[3]) > 0:
            estacionesSlots.append(station)
        if distPunts <= 1.0 and int(station[4]) > 0:
            estacionesBikes.append(station)


    print "Restaurant:"
    print restaurante
    print "Estacions amb llocs lliures:"
    estacionesSlots.sort(key=lambda x:x[5])
    for estSlot in estacionesSlots:
        print estSlot

    print ""
    print "Estacions amb bicings lliures:"
    estacionesBikes.sort(key=lambda x:x[5])
    for estBike in estacionesBikes:
        print estBike

    print ""  
    estacionesSlots = []
    estacionesBikes = []




