#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask.ext.googlemaps import GoogleMaps
from flask.ext.googlemaps import Map

import ApiTwitter 
import twitter
import io
import json
from flask import request
app=Flask(__name__)
GoogleMaps(app)
global termino 
termino=[]

#Definimos con variables los datos que queremos obtener de twitter
#es decir, los tweet que hablen del Atletico cerca de conil

@app.route("/buscar", methods=['POST'])
def buscar():
	termino = request.form['text'] 

	q=termino
	geocode='36.2780990,-6.0862070,100km'

	twitter_api= ApiTwitter.oauth_login()
	tweets= twitter_api.search.tweets(q=q, geocode=geocode)
	ApiTwitter.save_json("Gtweets",tweets)

	#Recuperamos el fichero json para trabajar con los datos obtenidos de twitter
	datos = json.loads(open('Gtweets.json').read())
	lista=[]
	for result in datos["statuses"]:
	    if result["coordinates"]:
		xy=[result["coordinates"].values()[1][1],result["coordinates"].values()[1][0]]
		lista.append(xy)
	mymap = Map(
		identifier="view-side",
		lat=36.2780990,
		lng=-6.0862070,
		markers=lista,
		style="height:700px; width:700px;margin:0;"
	    )
	return render_template('template.html', mymap=mymap)
	 

@app.route("/")
def index():
	return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

