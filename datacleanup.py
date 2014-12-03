import numpy as np
import csv
import json
import urllib2
import urllib

def loadData(filename):
	data = []
	with open(filename, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
        		data.append(row)
	#data = np.genfromtxt(filename, delimiter=',', dtype=None, loose=True, invalid_raise=False)
	return data

def saveData(data, filename, delim='|', header=None):
	writer = csv.writer(open(filename, 'w'), delimiter=delim)
	if header != None:
		writer.writerow(header)
	for row in data:
		writer.writerow(row)

def getURL(address):
	address = address.replace(" ", "+")
	return "https://maps.googleapis.com/maps/api/geocode/json?address="+address+"&key=AIzaSyA6_ynPzZCQLtdBYNQmszxBlP7iFd5TjWQ"

def getCoordinates(address):
	url = getURL(address)
	#print url
	data = json.load(urllib2.urlopen(url))
	#print data
	if(data["status"] == "OK"):
		lat = data["results"][0]["geometry"]["location"]["lat"]
		lng = data["results"][0]["geometry"]["location"]["lng"]
		return (lat, lng)
	else:
		return ("","")

def removeInvalidGPS():
	data = np.genfromtxt("data/data/final_dataDec.csv", delimiter=',')
	count = 0
	for i in xrange(data.shape[0]-1, 0, -1):
		if data[i, 16] > -70 or data[i, 16]< -80 or data[i, 17] < 40 or data[i, 17] > 50:
			np.delete(data, i, 0)
			count += 1
	header = "not_sold,2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002,num_bed,year_built,longitude,latitude,num_room,num_bath,living_area,house,commercial,plex,bungalow,chalet,loft,hotel,restauration,condo,num_parking,accessible_buildings,family_quality,art_expos,emergency_shelters,emergency_water,Facilities,fire_stations,Cultural,Monuments,police_stations,Vacant,Free_Parking,askprice"
	saveData(data, "data/data/final_dataDec.csv", ',', header)
	
if __name__=='__main__':
	data = loadData("Dec1Data.csv")
	print len(data)
	final_data = []
	for d in data:
		print len(final_data)
		if(d[5] == 0 or d[5] == ""):
			(lat, lng) = getCoordinates(d[10])
			d[5] = lng
			d[11] = lat
		final_data.append(d)
	
	saveData(final_data, "final_data_fixed-cleanDec.csv")
		
