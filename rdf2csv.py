# Cristian Davila Carmona
# Primer script

#!/usr/bin/python

import sys
import csv

from HTMLParser import HTMLParser

allrest=[]

class restaurant:     


    def afegir_nom(self,nom):
        self.nom = nom

    def afegir_adaptat(self, adaptat):
        self.adaptat = adaptat

    def afegir_address(self, address):
        self.address = address

    def afegir_latitude(self, latitude):
        self.latitude = latitude

    def afegir_longitude(self, longitude):
        self.longitude = longitude

    def afegir_telefon(self,telefon):
            if hasattr(self,'telefon'):
                    self.telefon.append(telefon)
            else:
                    self.telefon = []
                    self.telefon.append(telefon)

    def afegir_district(self, district):
        self.district = district

    def afegir_email(self, email):
        self.email = email

    def afegir_addressWeb(self, web):
        self.web = web

        
# creem una subclasse i sobreescribim el metodes del han
class MHTMLParser(HTMLParser):

    crest = restaurant()
    ctag = ""

    def handle_starttag(self, tag, attrs):
        self.ctag = tag
        if tag == 'v:vcard':
            self.crest = restaurant()

        if tag == 'v:url':
            for name, value in attrs:
                if name == 'rdf:resource':
                    self.crest.afegir_addressWeb(value)

        if tag == 'rdf:description':
            for name, value in attrs:
                if name == 'rdf:about':
                    self.crest.afegir_email(value)

    def handle_endtag(self, tag):
        self.ctag = ""
        if tag == 'v:vcard':
            allrest.append(self.crest)


    def handle_data(self, data):
        if self.ctag == 'v:fn':
            self.crest.afegir_nom(data)

        elif self.ctag == 'xv:adapted':
            self.crest.afegir_adaptat(data)

        elif self.ctag == 'v:street-address':
            self.crest.afegir_address(data)

        elif self.ctag == 'v:latitude':
            self.crest.afegir_latitude(data)

        elif self.ctag == 'v:longitude':
            self.crest.afegir_longitude(data)

        elif self.ctag == 'rdf:value':
            self.crest.afegir_telefon(data)

        elif self.ctag == 'xv:district':
            self.crest.afegir_district(data)


f = open('restaurants.rdf', 'rb') # obre l'arxiu
rdfSource = f.read()                            
f.close()

restaurantfile  = open('restaurants.csv', "wb")
restaurantwriter = csv.writer(restaurantfile)

parser = MHTMLParser()
parser.feed(rdfSource)


name = 'NAME'
add = 'ADDRESS'
lat = 'LATITUDE'
lon = 'LONGITUDE'
district = 'BARRI'
telefon1 = 'TELEFON 1'
telefon2 = 'TELEFON 2'
email = 'EMAIL'
web = 'WEB'

restaurantwriter.writerows([[name,add,lat,lon,district,telefon1, telefon2, email,web]])

for r in allrest:
    name = [r.nom]
    lon = [r.longitude]
    lat = [r.latitude]
    if hasattr(r, 'address'):
        add = [r.address]
    else:
        add = ['--']

    if hasattr(r, 'district'):
        district = [r.district]
    else:
        district = ['--']


    if hasattr(r, 'web'):
        web = [r.web]
    else:
        web = ['--']



    telefon1 = ['--']
    telefon2 = ['--']

    if hasattr(r, 'telefon'):
        if (r.telefon[0])[0]=='+':
            telefon1 = [r.telefon[0]]


    if hasattr(r, 'telefon'):
        if len(r.telefon) == 2:
            if (r.telefon[1])[0]=='+':
                telefon2 = [r.telefon[1]]




    if hasattr(r, 'email'):
        seg = r.email[7::]
        email = [seg]
    else:
        email = ['--']

    info = name+add+lat+lon+district+telefon1+telefon2+email+web

    restaurantwriter.writerows([info])


restaurantfile.close()

