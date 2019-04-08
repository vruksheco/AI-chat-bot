import requests
import json
import webbrowser
import datetime

def get_distance(origin,destination) :		#to get the distance and time of travel between to places 
											#arguents - names of origin and destination 
											#Return  - 0 -> Failure -1 -> Success
	#Preparing the URL with the corresponding API_KEY and Origin and Destination
	URL = "https://maps.googleapis.com/maps/api/distancematrix/json"
	api_key = "AIzaSyAc8sSX5nvupgyKP51NOLz3iy2bVs9eVRw"
	PARAMS = {'units':"imperial",'origins' : origin,'destinations':destination,'key' : api_key}
	#sending the get request
	r = requests.get(url = URL, params = PARAMS)
	#parsing the JSON response
	data = r.json()
	
	if data['destination_addresses'][0] is None : #to verify if the destination is valid
		print("Please enter a valid or detailed description of Destination")
	elif data['origin_addresses'][0] is None :	  #to verify if the origin entered is valid
		print("Please enter a valid or detailed description of Source")
	elif data['rows'][0]['elements'][0]['status'] == "ZERO_RESULTS" :  #to check if a path exists
		print("I am afraid that there is no route through road from " + data['origin_addresses'][0] + " to " + data['destination_addresses'][0])
	else :
		distance = data['rows'][0]['elements'][0]['distance']['text']
		time = data['rows'][0]['elements'][0]['duration']['text']
		print("Source :",data['origin_addresses'][0])					#printing the details on the screen
		print("Destination",data['destination_addresses'][0])
		print("Distance is : ",distance)
		print("Estimated time is : ",time)

def get_location(location) :			#to get the lattitude,longitude and complete address details by the name of the place
										#argument - Name the place 
										#return = 0->unable to fetch the exact details of the place  1-> Success
	#Preparing the URL with the corresponding API_KEY and Location
	URL = "https://maps.googleapis.com/maps/api/geocode/json"
	api_key = "AIzaSyAX9WQSnengdMPvq8J0BiPltK4Gae-Z9Zo"
	PARAMS = {'address':location,'key' : api_key}

	r = requests.get(url = URL, params = PARAMS)

	if r.status_code != 200 :
		print("Sorry unable to reach")
	else :
		#parsing the JSON response
		data = r.json()
		if data['status'] == "ZERO_RESULTS" :	
			print("Please enter a valid or detailed description of Destination")
			return 0
		else :
			latitude = data['results'][0]['geometry']['location']['lat']
			longitude = data['results'][0]['geometry']['location']['lng']
			formatted_address = data['results'][0]['formatted_address']
			#print("Is this the location %s,%s"%(location,formatted_address))
			print(formatted_address)
			return 1

def get_weather(location,mode,num) :	#to get the weather at a place 
										#arguments : location-place name to know the weather | mode-current/hourly/daily
										#return = 0-> place not found 1->success
	latitude = ""
	longitude = ""
	#Preparing the URL with the corresponding API_KEY and Location
	URL = "https://maps.googleapis.com/maps/api/geocode/json"
	api_key = "AIzaSyAX9WQSnengdMPvq8J0BiPltK4Gae-Z9Zo"
	PARAMS = {'address':location,'key' : api_key}

	r = requests.get(url = URL, params = PARAMS)

	if r.status_code != 200 :
		print("Sorry unable to reach")
	else :
		#parsing the JSON response
		data = r.json()
		if data['status'] == "ZERO_RESULTS" :		#if the description is not detailed or if the place doesnot exist
			print("Please enter a valid or detailed description of Destination")
			return 0
		else :
			#extracting and displaying the corresponding information
			latitude = data['results'][0]['geometry']['location']['lat']
			longitude = data['results'][0]['geometry']['location']['lng']
			formatted_address = data['results'][0]['formatted_address']
			print(formatted_address)
	#Preparing the URL with the corresponding API_KEY, Lattitude and Longitude
	URL = "https://api.darksky.net/forecast/36fdd279bf55a5b97542bab1b5ccbbd7/" + str(latitude) + "," + str(longitude)

	r = requests.get(url = URL, params = None)

	if r.status_code != 200 :
		print("Sorry unable to reach")

	elif mode == 0 :  #gets the current weather conditions
		#parsing the JSON response
		data = r.json()
		temperature = data['currently']['temperature']
		humidity = data['currently']['humidity']
		apparentTemperature = data['currently']['apparentTemperature']
		print("\nTemparature : %s F\nHumidity : %s\nFeels like : %s F\n"%(temperature,humidity,apparentTemperature))
		return 1

	elif mode == 1 : #hourly #num is the number of hours for the forecast
		#parsing the JSON response
		data = r.json()
		i = 0
		print("\n" + data['hourly']['summary'] + "\n")
		for i in range(num) :
			temperature = data['hourly']['data'][i]['temperature']
			humidity = data['hourly']['data'][i]['humidity']
			apparentTemperature = data['hourly']['data'][i]['apparentTemperature']
			time = data['hourly']['data'][i]['time']
			print(datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S'))
			print("Temparature : %s F   Humidity : %s   Feels like : %s F\n"%(temperature,humidity,apparentTemperature))
		return 1

	elif mode == 2 :#weekly #it gives details about rest of the week or num(argument) number of days, which ever is less

		#r = requests.get(url = URL, params = None)
		data = r.json()
		i = 0
		print("\n" + data['daily']['summary'] + "\n")
		previous = ""
		for i in range(len(data['daily']['data'])) :
			time = data['hourly']['data'][i]['time']
			if previous != datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d') :
				temperatureHigh = data['daily']['data'][i]['temperatureHigh']
				humidity = data['daily']['data'][i]['humidity']
				temperatureLow = data['daily']['data'][i]['temperatureLow']
				print(datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d'))
				print("Temparature High: %s F   Temperature Low : %s F   Humidity : %s\n"%(temperatureHigh,temperatureLow,humidity))
				previous = datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d')
				i = i + 1
				if i == num :
					break
		return 1

def get_meaning(word) :				#to get all possible meanings for a word
									#arguments : word -> word about which meanings are required
	#Preparing the URL with the corresponding API_KEY and Word
	app_id = '1c7374ed'
	app_key = 'ad782dd3f872f46aa40898a9d6ef807e'

	language = 'en'
	url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word.lower()
	r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

	if r.status_code != 200 :
		print("Sorry unable to reach")

	else :

		print("\nMeaning for " + word + " : ")
		#parsing the JSON response
		data = r.json()
		
		for i in range(len(data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'])) :
			print(str(i+1) + " : " + data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][i]['definitions'][0])
			
def get_ant_syn(word, lel) :		#to get all the synonyms or antonyms
									#arguents : word , lel - 2->antonyms 1->synonyms
	#Preparing the URL with the corresponding API_KEY and Word
	app_id = '1c7374ed'
	app_key = 'ad782dd3f872f46aa40898a9d6ef807e'

	language = 'en'
	url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word.lower() + '/synonyms;antonyms'
	r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

	if r.status_code != 200 :
		print("Sorry unable to reach")

	else :
		#parsing the JSON response
		data = r.json()
		if lel == 2 :
			print("It cound be :")
			for i in range(len(data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['antonyms'])) :
				print(data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['antonyms'][i]['id'])
		else :
			print( "\nSynonyms of " + word)
			for j in range(len(data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['synonyms'])) :
				print(data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['synonyms'][j]['id'])

def get_what_is(word) :			#to open browser and search for a words
	#Preparing the URL to be triggered in the browser
	url = "http://www.google.com/?q=" + word
	webbrowser.open_new(url)

#get_distance("Hyderabad","Karimnagar")
#get_location("Raigbdfiagdfay")
#get_weather("BITS Pilani Hyderabad Campus",0,10)
#get_meaning("alpha")
#get_what_is("Boon")
#get_ant_syn("boon")
