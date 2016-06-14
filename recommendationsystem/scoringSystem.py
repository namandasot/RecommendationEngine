## Budget Above 3cr Done
## Movein :  Anytime and > 3yrs
## Ready for possesion


import numpy as np

class scroingSystemForWebsite:

	def __init__(self): 
		self.budget = 'Minimum_Price'  #budget in searchParams 
		self.price = 'price'  #price in past and reco properties
		self.amenities = 'amenities' 
		self.bhk = 'No_Of_Bedroom'
		self.posession = 'Possession'
		self.longitude = 'Map_Longitude'
		self.latitude = 'Map_Latitude'
		self.locationName = 'locality_name'
		self.textStr = 'text'
		self.scoreStr = 'score'
		self.flagStr = 'flag'
		self.posessionDate = "posessionDate"
		self.projectNumber = "Project_No"
		self.projectConfigNumber = "Project_Config_No"
		self.budgetMaxInput = "30000000"
		self.posessionMaxInput = 365*3


		self.fullScoreDistInKm = 5
		self.leastScoreDistInKm = 20
		self.weights = [1,0.8,0.6,0.4,0.3,0.2,0.1,0,0,0,0,0,0,0,0]
		self.scoringMax  = 100
		self.scoringMin = 10
		self.scoringThresholdDown = 0.2
		self.scoringThresholdUp = 1.2
		self.scoringThresholdUp50 =  1.4
		self.currSearchWeight = 1
		self.threeMonths = 95
		self.sixMonths = 185
		self.oneYear = 370
		self.twoYear = 750
		self.fiveYear = 1900
		self.scoreScaling = 10.0


	# Search Params : 

	def getScores(self,searchParams,pastPropAttrList,recoPropAttrList,preferanceList ):


		# First, scores will be calculated out of 100 and then changed according to their order
		projectNo = map (lambda x:x[self.projectNumber],recoPropAttrList)
		projectConfigNo = map (lambda x:x[self.projectConfigNumber],recoPropAttrList)
		
		amenitiesScore = []

		""" Location"""
		if(searchParams[0][self.locationName]):
			locationScore =  self.getLocationScore(searchParams,pastPropAttrList,recoPropAttrList)

		""" Amenities """
		if(searchParams[0][self.amenities]):
			amenitiesScore = self.getAmenitiesScore(searchParams,recoPropAttrList)

		""" BUDGET """
		if(searchParams[0][self.budget]):
			budgetScore = self.getBudgetScore(searchParams,pastPropAttrList,recoPropAttrList)

		""" BHK """
		if(searchParams[0][self.bhk]):
			bhkScore = self.getBHKScore(searchParams,pastPropAttrList,recoPropAttrList)

		""" Posession """
		if(searchParams[0][self.posession]):
			posessionScore = self.getPosessionScore(searchParams,recoPropAttrList)

		# print projectNo
		# print "locationScore " ,locationScore
		# print "amenitiesScore " , amenitiesScore
		# print "budgetScores ",budgetScores
		# print "bhkScore ",bhkScore
		# print "posessionScore ",posessionScore

		listFinal = []
		for i,projectNum in enumerate(projectNo):
			dictionary1 = {}
			finalScore = 0
			factorDiv = 0
			if(searchParams[0][self.amenities]):
				dictionary1["amenities"]=amenitiesScore[i]
				finalScore = finalScore + (5-preferanceList.index("amenities"))*amenitiesScore[i]["score"]
				factorDiv = factorDiv + 5 - preferanceList.index("amenities")

			if(searchParams[0][self.locationName]):
				dictionary1["location"]=locationScore[i]
				finalScore = finalScore + (5 - preferanceList.index("location"))*locationScore[i]["score"]
				factorDiv = factorDiv + 5 - preferanceList.index("location")

			if(searchParams[0][self.bhk]):
				dictionary1["bhk"]=bhkScore[i]
				finalScore = finalScore + (5-preferanceList.index("bhk"))*bhkScore[i]["score"]
				factorDiv = factorDiv + 5 - preferanceList.index("bhk")

			if(searchParams[0][self.posession]):
				dictionary1["possession"]=posessionScore[i]
				finalScore = finalScore + (5-preferanceList.index("possession"))*posessionScore[i]["score"]
				factorDiv = factorDiv + 5 - preferanceList.index("possession")

			if(searchParams[0][self.budget]):
				dictionary1["budget"]= budgetScore[i]
				finalScore = finalScore + (5-preferanceList.index("budget"))*budgetScore[i]["score"]
				factorDiv = factorDiv + 5 - preferanceList.index("budget")
			
			# print finalScore
			# print factorDiv
			score = float(finalScore)/factorDiv
			# print score
			score = min(9.8,score)
			dictionary1[ "total_score"] = score

			#dictionary1 = {"budget": budgetScores[i],"location": locationScore[i],"bhk":bhkScore[i],"possession": posessionScore[i],"amenity" : amenitiesScore[i]}
			dictionary = {self.projectNumber : projectNum, self.projectConfigNumber : projectConfigNo[i] , "relevance_score":dictionary1}
			listFinal.append(dictionary)


		
		# for a in listFinal:
		# 	for b in a:
		# 		print b , a[b]

		return listFinal


	def getAmenitiesScore(self,searchParams,recoPropAttrList):

		searchAmenities = searchParams[0][self.amenities]
		recoAmenities = map (lambda x:x[self.amenities],recoPropAttrList)
		flag = 0
		text = ""
		# print searchAmenities
		totalWantedAmenities = len(searchAmenities)
		amenitiesScoreList  = []

		# print recoAmenities
		# print "a"
		for amenity in recoAmenities:
			numAmenities = 0
			falseList = []
			# print amenity
			for a in searchAmenities :
				if( a in amenity):
					numAmenities = numAmenities+1
				else : 
					falseList.append(a)

			if(len(falseList) == 0):
				text = "All of your required amenities are present"
				flag = 1
			else:
				text = "Sorry, the property does not have " + str(', '.join(falseList))  
				flag  = 0



			match =  len(set(searchAmenities).intersection(amenity))

			score = float(match)/totalWantedAmenities*self.scoringMax

			# print text
			# print 
			# print score
			score = score/self.scoreScaling
			# print score

			dictionary = {self.textStr : text, self.scoreStr : score, self.flagStr : bool(flag)}
			amenitiesScoreList.append(dictionary)
		# print "done"
		return amenitiesScoreList



	def getBHKScore(self,searchParams,pastPropAttrList,recoPropAttrList):
		searchBHK = searchParams[0][self.bhk]
		pastBHK = map (lambda x:x[self.bhk],pastPropAttrList)
		recoBHK = map (lambda x:x[self.bhk],recoPropAttrList)
		# print "BHK"
		# print pastBHK
		score = 0
		flag = 0
		text = ""
		bhkScoreList = []
		for bhk in recoBHK:
			if(bhk >= searchBHK):
				score =  self.scoringMax
				if(bhk == searchBHK):
					text = "Congrats, thats the " + str(searchBHK) + " BHK you wanted"
				else:
					text = "Hurray!!! There's an upgrade. It's a" + str(bhk)+ " BHK"

				flag = 1
			else :
				if(bhk < searchBHK-1):
					score = 0
				else:
					if(bhk in pastBHK) : 
						factor = (pastBHK.index(bhk) + 1)*2
						# print factor
						score = max(self.scoringMax/factor , self.scoringMin)
				flag = 0
				text = "Alas! It's only a " + str(bhk) + " BHK"

			score = score/self.scoreScaling
			dictionary = {self.textStr : text, self.scoreStr : score, self.flagStr : bool(flag)}
			bhkScoreList.append(dictionary)

		return bhkScoreList


	def getBudgetScore(self,searchParams,pastPropAttrList,recoPropAttrList):
		searchBudget = searchParams[0][self.budget]
		pastBudget = map (lambda x:x[self.price],pastPropAttrList)
		recoBudget = map (lambda x:x[self.price],recoPropAttrList)

		pastBudget = np.array(pastBudget)
		# print 
		# print pastBudget
		budgetMeanAndStd = self.getModifiedStdDev(pastBudget,searchBudget)
		# print budgetMeanAndStd
		budgetMean = budgetMeanAndStd[0]
		budgetStd = budgetMeanAndStd[1]

		budgetScoreList  = []
		flag = 0
		text = ""
		for budget in recoBudget:
			score = 0
			flag = 0

			if(searchBudget >= self.budgetMaxInput):
				if(budget >= searchBudget):
					score = self.scoringMax
					text = "Congrats, the Property meets your budget requirements"
					flag = 1
				else:
				 	score = self.getLineValue((self.budgetMaxInput),(self.budgetMaxInput)*self.scoringThresholdDown,budget)
					score = min(score,self.scoringMax)
					text = "Property is within your budget"
					if(score >= 80):
						flag = 1
						text = "Congrats, the Property meets your budget requirements"
				continue


			# print
			# print "in recobudget" , budget
			if(budget >= budgetMean):

				if(budget <= searchBudget):
					score = self.scoringMax
					text = "Congrats, the Property is within your budget"
					flag = 1

				else:
					score = self.getLineValue((budgetMean + budgetStd/2),(budgetMean + budgetStd/2)*self.scoringThresholdUp,budget)
					score = min(score,self.scoringMax)
					if(score > 85):
						text = "Property is within your budget"
						flag = 1
					elif(score > 60):
						text = "Property is slightly above your budget"
						flag  = 0
					else:
						text = "Property is above your budget"
						flag = 0


			
			#		budget < budgetMean
			else:
				if(budget > searchBudget ):
					score = self.scoringMax
					text = "Property is within your current search budget Range"
					flag = 1

				else:
					score = self.getLineValue((budgetMean - budgetStd/2),(budgetMean - budgetStd/2)*self.scoringThresholdDown,budget)
					score = min(score,self.scoringMax)
					text = "Property is within your budget"

					if(score > 80):
						flag = 1
					else:
						flag = 0

			score = max(self.scoringMin , score)
			score = score/self.scoreScaling
			dictionary = {self.textStr : text, self.scoreStr : score, self.flagStr : bool(flag)}
			budgetScoreList.append(dictionary)

		return budgetScoreList



	def getDistanceinKM(self,lat1,lon1,lat2,lon2):
		R = 6371  # radius of the earth in km
		lat1 = np.radians(float(lat1))
		lat2 = np.radians(float(lat2))
		lon1 = np.radians(float(lon1))
		lon2 = np.radians(float(lon2))
		x = (lon2 - lon1) * np.cos( 0.5*(lat2+lat1) )

		y = lat2 - lat1
		d = R * np.sqrt( x*x + y*y )
		return d



		#slope = 1 for positive slope ie less budget
	def getLineValue(self,p1x,p2x,query):
		p1y = self.scoringMax
		p2y = self.scoringMin
		slope = float((p1y - p2y))/(p1x - p2x)
		constant = float(((p2y*p1x) - (p1y*p2x))) / (p1x - p2x)
		return ((slope * query) + constant)

	def getLineValueAll(self,p1x,p1y,p2x,p2y,query):
		# p1y = self.scoringMax
		# p2y = self.scoringMin
		slope = float((p1y - p2y))/(p1x - p2x)
		constant = float(((p2y*p1x) - (p1y*p2x))) / (p1x - p2x)
		return ((slope * query) + constant)


	def getLocationScore(self,searchParams,pastPropAttrList,recoPropAttrList):

		# searchLatitude = searchParams[0][self.latitude]
		# searchLongitude = searchParams[0][self.longitude]
		
		recoLatitude = map (lambda x:x[self.latitude],recoPropAttrList)		
		recoLongitude = map (lambda x:x[self.longitude],recoPropAttrList)
		recoLocation = map (lambda x:x[self.locationName],recoPropAttrList)
		locationScoreList = []
		flag = 0
		text = ""
		for lat,lon,loc in zip(recoLatitude,recoLongitude,recoLocation):
			
			flag =0
			minDist = 1000
			minDistLocation = searchParams[0][self.locationName]

			for searchResults in searchParams:
				searchLatitude = searchResults[self.latitude]
				searchLongitude = searchResults[self.longitude]
				searchLocation = searchResults[self.locationName]

				if(searchLocation.lower() in loc.lower()  ):
					flag = 1
					minDist = 0
					minDistLocation = loc
					
					break

				distanceInKM = self.getDistanceinKM(lat,lon,searchLatitude,searchLongitude)

				if(distanceInKM < minDist):
					minDist = distanceInKM
					minDistLocation = searchLocation

			if(flag == 1):
				score = self.scoringMax
				loc = loc.split(",")[0]
				text = "Congrats! The Property is in " + loc


			else :
				score = self.getLineValue(0,self.leastScoreDistInKm,minDist)
				score = max(score,self.scoringMin)
				loc = loc.split(",")[0]
				text = "Sorry the property is in " + loc + ", but is only " + str(round(minDist,1)) + "km away from " + minDistLocation

			score = score/self.scoreScaling
			dictionary = {self.textStr : text, self.scoreStr : score , self.flagStr : bool(flag)}
			locationScoreList.append(dictionary)

		return locationScoreList

	def getModifiedStdDev(self,myArray,currSearch):

		lengthArray = len(myArray)
		tempWeight = self.weights[:lengthArray]
		tempWeight = np.array(tempWeight)
	

		#skewedMean =  sum(myArray*tempWeight)/sum(tempWeight)
		skewedMean =  (sum(myArray*tempWeight)+ currSearch * self.currSearchWeight)/(sum(tempWeight)+self.currSearchWeight)
		# print skewedMean
		skewedVar = myArray - skewedMean
		skewedVar = skewedVar * tempWeight
		skewedVar = skewedVar**2
		# skewedVar = sum(skewedVar)
		skewedVar = sum(skewedVar) + (((currSearch - skewedMean)*self.currSearchWeight)**2)
		# skewedVar = skewedVar/lengthArray
		skewedVar = skewedVar/(lengthArray+1)

		skewedStd = np.sqrt(skewedVar)
		returnList = [skewedMean, skewedStd]

		return returnList


	def getPosessionScore(self,searchParams,recoPropAttrList):
		searchPosession = searchParams[0][self.posession]
		recoPosession = map (lambda x:x[self.posession],recoPropAttrList)
		recoPosessionDate = map (lambda x:x[self.posessionDate],recoPropAttrList)
		posessionScoreList = []
		flag = 0
		text = ""
		for posession,posessionDate in zip(recoPosession,recoPosessionDate):
			flag = 0
			if(searchPosession >= self.posessionMaxInput):
				if(posession >= searchPosession ):
					flag = 1
					score = self.scoringMax
					text = "This home will be yours after " + posessionDate

				else:
					score = self.getLineValue((self.posessionMaxInput),0,posession)
					score = min(score,self.scoringMax)
					text = "Property will be yours by "+ posessionDate
					if(score >= 80):
						flag = 1
						


				continue

			if(posession <= searchPosession):
				score = self.scoringMax
				flag  = 1 

				text = "This home can be yours after " + posessionDate
				if(posessionDate == "Ready for Possession"):
					text = "This home is " + posessionDate
			else:
				diff = posession- searchPosession
				if(diff < self.oneYear):
					score = self.getLineValueAll(0,100,self.oneYear,50,diff)
					score = min(score,self.scoringMax)
					score = max(score,self.scoringMin)
				elif(diff < self.fiveYear):
					score = self.getLineValueAll(self.oneYear,50,self.fiveYear,10,diff)
					score = min(score,self.scoringMax)
					score = max(score,self.scoringMin)
				else:
					score = 0



				"""
				if(diff <= self.threeMonths):
					score = self.scoringMax / 1.3
				elif(diff <= self.sixMonths):
					score = self.scoringMax / 2
				elif (diff <= self.oneYear):
					score = self.scoringMax / 4
				elif (diff < self.twoYear):
					score = self.scoringMin
				else:
					score = 0
				"""

				text = "This home can be yours only after " + posessionDate
				if(posessionDate == "Ready for Possession"):
					text = "This home is " + posessionDate , " ", diff
					# flag =1
					# score = self.scoringMax
			score = score/self.scoreScaling
			dictionary = {self.textStr : text, self.scoreStr : score, self.flagStr : bool(flag)}
			posessionScoreList.append(dictionary)
		return posessionScoreList



import time
if __name__ == '__main__':
	searchParams = [{"Category":None,"Built_Up_Area":900,"Project_No":None,"No_Of_Bathroom":None,"Minimum_Price":9000000,"PricePerUnit":None,"No_Of_Bedroom":2,"Possession":90,"Project_City_Name":"mumbai","amenities":["Swimming Pool","Gym"],"Map_Longitude":"72.827567000000000","Project_config_No":None,"locality_name":"andheri","Map_Latitude":"19.194291000000000","No_Of_Balconies":None},{"Category":None,"Built_Up_Area":900,"Project_No":None,"No_Of_Bathroom":None,"Minimum_Price":9000000,"PricePerUnit":None,"No_Of_Bedroom":2,"Possession":90,"Project_City_Name":"mumbai","amenities":["Swimming Pool","Gym"],"Map_Longitude":"72.832754686438760","Project_config_No":None,"locality_name":"malad","Map_Latitude":"19.206685585502232","No_Of_Balconies":None},{"Category":None,"Built_Up_Area":900,"Project_No":None,"No_Of_Bathroom":None,"Minimum_Price":9000000,"PricePerUnit":None,"No_Of_Bedroom":2,"Possession":90,"Project_City_Name":"mumbai","amenities":["Swimming Pool","Gym"],"Map_Longitude":"72.852032000000000","Project_config_No":None,"locality_name":"goregaon","Map_Latitude":"19.221384000000000","No_Of_Balconies":None}]
	pastPropAttrList = [{'price':1000000,'No_Of_Bedroom':3,'posession':1},{'price':900000,'No_Of_Bedroom':2,'posession':1},{'price':900000,'No_Of_Bedroom':3,'posession':1},{'price':900000,'No_Of_Bedroom':2,'posession':1}]
	recoPropAttrList = 	[{'Possession': 594, 'Built_Up_Area': 680, 'Project_No': 2236, 'amenities': [u'Club house', u"Children's Play Area", u'24 Hours Security', u'Yoga', u'Tennis Court', u'Swimming Pool', u'Spa', u'Sauna', u'Restaurant', u'Rain Water Harvesting', u'Pool Table', u'Park', u'Lifts', u'Library', u'Landscape Garden', u'Jogging Track', u'Jacuzzi', u'Indoor Games', u'Health Facilities', u'Gym', u'Fire Fighting Arrangements', u'Earthquake Resistant'], 'price': 6460000, 'Project_Config_No': 48213, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2017', 'Map_Longitude': u'72.827567000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad West', 'locality_name': u'Malad West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.194291000000000'}, {'Possession': 198, 'Built_Up_Area': 700, 'Project_No': 6496, 'amenities': [u'Rain Water Harvesting', u'24 Hours Security', u'Lifts', u'Parking'], 'price': 6300000, 'Project_Config_No': 27985, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.813032868700000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad West', 'locality_name': u'Malad West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.178373065700000'}, {'Possession': 594, 'Built_Up_Area': 868, 'Project_No': 11393, 'amenities': [u'Party Hall', u'24 Hours Power Backup', u"Children's Play Area", u'Club house', u'Garden', u'Gym', u'Indoor Games', u'Intercom'], 'price': 8549800, 'Project_Config_No': 41639, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2017', 'Map_Longitude': u'72.821083100000000', 'No_Of_Bedroom': 2.0, 'Project_Area_Name': u'Kandivali West', 'locality_name': u'Kandivali West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.203794400000000'}, {'Possession': 15, 'Built_Up_Area': 719, 'Project_No': 1521, 'amenities': [u'Video Door Intercom', u'Swimming Pool', u'Parking', u'Park', u'Lifts', u'Landscape Garden', u'Gym', u'Club house', u"Children's Play Area", u'24 Hours Security'], 'price': 9311050, 'Project_Config_No': 36963, 'Project_City_Name': u'Mumbai', 'posessionDate': u'May 2016', 'Map_Longitude': u'72.818635000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Kandivali West', 'locality_name': u'Kandivali West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.207123000000000'}, {'Possession': 229, 'Built_Up_Area': 485, 'Project_No': 6199, 'amenities': [u'Club house', u'Park'], 'price': 6402000, 'Project_Config_No': 37630, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2016', 'Map_Longitude': u'72.846489000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Goregaon West', 'locality_name': u'Goregaon West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.156782000000000'}, {'Possession': 106, 'Built_Up_Area': 475, 'Project_No': 7727, 'amenities': [u'Fire Fighting Arrangements', u'Garden', u'Lifts', u'Parking', u'Rain Water Harvesting'], 'price': 6887500, 'Project_Config_No': 32466, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.839944000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Goregaon West', 'locality_name': u'Goregaon West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.165087000000000'}, {'Possession': 594, 'Built_Up_Area': 720, 'Project_No': 4876, 'amenities': [u'Restaurant', u'Party Hall', u'Park', u'Library', u'Landscape Garden', u'Jogging Track', u'Indoor Games', u'Gym', u'Club house', u"Children's Play Area", u'Amphitheatre', u'Sauna', u'Swimming Pool', u'Tennis Court', u'Wifi Coverage', u'Yoga'], 'price': 7560000, 'Project_Config_No': 20336, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Contact Seller For Possession', 'Map_Longitude': u'72.827919000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Kandivali West', 'locality_name': u'Kandivali West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.194557000000000'}, {'Possession': 226, 'Built_Up_Area': 645, 'Project_No': 12833, 'amenities': [u'24 Hours Power Backup', u'24 Hours Security', u"Children's Play Area", u'Lifts', u'Security System'], 'price': 9400000, 'Project_Config_No': 41989, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2016', 'Map_Longitude': u'72.832754686400000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Kandivali West', 'locality_name': u'Kandivali West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.206685585500000'}, {'Possession': 594, 'Built_Up_Area': 775, 'Project_No': 20465, 'amenities': [u'24 Hours Power Backup', u'Fire Fighting Arrangements', u'Gas Line', u'Gym', u'Lifts', u'Security System'], 'price': 7962500, 'Project_Config_No': 54931, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2017', 'Map_Longitude': u'72.863927728800000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad East', 'locality_name': u'Malad East, Western Suburb, Mumbai', 'Project_Suburb_Name': u'Western Suburb', 'Map_Latitude': u'19.184186000000000'}, {'Possession': 410, 'Built_Up_Area': 997, 'Project_No': 176, 'amenities': [u'Jogging Track', u'Lifts', u'Park', u'Podium Car Parking', u'Sauna', u'Security System', u'Swimming Pool', u'Tennis Court', u'Video Door Intercom', u'Gym', u'Cricketnet', u'Club house', u'24 Hours Security', u"Children's Play Area"], 'price': 11500000, 'Project_Config_No': 61529, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Jun 2017', 'Map_Longitude': u'72.822090000000000', 'No_Of_Bedroom': 2.0, 'Project_Area_Name': u'Kandivali West', 'locality_name': u'Kandivali West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.205676000000000'}, {'Possession': 349, 'Built_Up_Area': 725, 'Project_No': 6906, 'amenities': [u'24 Hours Security', u'Club house', u'Gym', u'Landscape Garden', u'Lifts', u'Parking'], 'price': 10000000, 'Project_Config_No': 37896, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Apr 2017', 'Map_Longitude': u'72.841774000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad West', 'locality_name': u'Malad West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.182239000000000'}, {'Possession': 684, 'Built_Up_Area': 592, 'Project_No': 18154, 'amenities': [u'Indoor Games', u'Gym', u'Lifts', u'Garbage Disposable System', u"Children's Play Area", u'Outdoor Games', u'Parking', u'24 Hours Security'], 'price': 8033440, 'Project_Config_No': 56296, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Mar 2018', 'Map_Longitude': u'72.862601728800000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad East', 'locality_name': u'Malad East, Western Suburb, Mumbai', 'Project_Suburb_Name': u'Western Suburb', 'Map_Latitude': u'19.182739733800000'}, {'Possession': 684, 'Built_Up_Area': 359, 'Project_No': 20291, 'amenities': [u'Gym', u'Intercom', u'Lifts', u'Park', u'Podium Car Parking', u'Swimming Pool', u'Wifi Coverage', u'24 Hours Power Backup', u'24 Hours Security', u'Club house'], 'price': 6856000, 'Project_Config_No': 53910, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Mar 2018', 'Map_Longitude': u'72.858999953400000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad East', 'locality_name': u'Malad East, Western Suburb, Mumbai', 'Project_Suburb_Name': u'Western Suburb', 'Map_Latitude': u'19.186225066500000'}, {'Possession': 229, 'Built_Up_Area': 370, 'Project_No': 5692, 'amenities': [u'Earthquake Resistant', u'24 Hours Security', u'Fire Fighting Arrangements', u'Lifts', u'Rain Water Harvesting', u'Parking', u'Security System'], 'price': 7500000, 'Project_Config_No': 24519, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2016', 'Map_Longitude': u'72.839528904300000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Goregaon West', 'locality_name': u'Goregaon West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.162141994500000'}, {'Possession': 199, 'Built_Up_Area': 650, 'Project_No': 8948, 'amenities': [u'24 Hours Security', u"Children's Play Area", u'Fire Fighting Arrangements', u'Gym', u'Intercom', u'Jogging Track', u'Lifts', u'Parking', u'Restaurant', u'Swimming Pool'], 'price': 10000000, 'Project_Config_No': 45531, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2016', 'Map_Longitude': u'72.836896058400000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Goregaon West', 'locality_name': u'Goregaon West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.165833120900000'}, {'Possession': 684, 'Built_Up_Area': 275, 'Project_No': 16152, 'amenities': [u'24 Hours Power Backup', u'Club house', u'Fire Fighting Arrangements', u'Garden', u'Gym', u'Intercom', u'Lifts', u'Park', u'Parking', u'Swimming Pool', u'Vastu Compliant', u'Wifi Coverage'], 'price': 4757500, 'Project_Config_No': 53971, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Mar 2018', 'Map_Longitude': u'72.865197177900000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad East', 'locality_name': u'Malad East, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.181591333000000'}, {'Possession': 168, 'Built_Up_Area': 304, 'Project_No': 20290, 'amenities': [u'Park', u'Lifts', u'Intercom', u'Garden', u'Club house', u'24 Hours Security', u'24 Hours Power Backup', u'Parking', u'Rain Water Harvesting', u'Vastu Compliant', u'Wifi Coverage'], 'price': 5289600, 'Project_Config_No': 53973, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Oct 2016', 'Map_Longitude': u'72.865094728800000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad East', 'locality_name': u'Malad East, Western Suburb, Mumbai', 'Project_Suburb_Name': u'Western Suburb', 'Map_Latitude': u'19.181282000000000'}, {'Possession': 106, 'Built_Up_Area': 680, 'Project_No': 17621, 'amenities': [u'Yoga', u'Tennis Court', u'Swimming Pool', u'Spa', u'Security System', u'Security Cabin', u'Landscape Garden', u'Lifts', u'Parking', u'Party Hall', u'Rain Water Harvesting', u'Basket Ball Court', u"Children's Play Area", u'Club house', u'Earthquake Resistant', u'Fire Fighting Arrangements', u'Gas Line', u'Gym', u'Indoor Games', u'Intercom'], 'price': 9520000, 'Project_Config_No': 54939, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Aug 2016', 'Map_Longitude': u'72.852954300000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Goregaon East', 'locality_name': u'Goregaon East, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.170920300000000'}, {'Possession': 594, 'Built_Up_Area': 805, 'Project_No': 18505, 'amenities': [u"Children's Play Area", u'Garden', u'Gym', u'Lifts', u'Intercom', u'Parking', u'Rain Water Harvesting'], 'price': 11100000, 'Project_Config_No': 50716, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2017', 'Map_Longitude': u'72.858419000000000', 'No_Of_Bedroom': 2.0, 'Project_Area_Name': u'Borivali East', 'locality_name': u'Borivali East, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.220513000000000'}, {'Possession': 136, 'Built_Up_Area': 458, 'Project_No': 14993, 'amenities': [u'Swimming Pool', u'Rain Water Harvesting', u'24 Hours Security', u"Children's Play Area", u'Club house', u'Gym', u'Parking', u'Lifts', u'Landscape Garden', u'Intercom', u'Indoor Games', u'24 Hours Power Backup'], 'price': 10076000, 'Project_Config_No': 43669, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.839082100000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad West', 'locality_name': u'Malad West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.182463800000000'}, {'Possession': 229, 'Built_Up_Area': 450, 'Project_No': 12022, 'amenities': [u'Indoor Games', u'24 Hours Power Backup', u"Children's Play Area", u'Garden'], 'price': 9000000, 'Project_Config_No': 43194, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2016', 'Map_Longitude': u'72.849569500000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Borivali West', 'locality_name': u'Borivali West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.222606100000000'}, {'Possession': 387, 'Built_Up_Area': 690, 'Project_No': 7115, 'amenities': [u'Security Cabin', u'Security System', u'Rain Water Harvesting', u'Lifts', u'Intercom', u'Gym', u'Fire Fighting Arrangements', u"Children's Play Area", u'24 Hours Security'], 'price': 9000000, 'Project_Config_No': 43293, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.869480000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Goregaon East', 'locality_name': u'Goregaon East, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.177190400000000'}, {'Possession': 594, 'Built_Up_Area': 432, 'Project_No': 19616, 'amenities': [u'24 Hours Power Backup', u'24 Hours Security', u"Children's Play Area", u'Fire Fighting Arrangements', u'Garden', u'Gym', u'Intercom', u'Lifts', u'Parking', u'Security System', u'Wifi Coverage'], 'price': 10000000, 'Project_Config_No': 51682, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2017', 'Map_Longitude': u'72.845003093300000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad West', 'locality_name': u'Malad West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.181821133200000'}, {'Possession': 45, 'Built_Up_Area': 650, 'Project_No': 6474, 'amenities': [u'Fire Fighting Arrangements', u'Gym', u'Jogging Track', u'Lifts', u'Park', u'Parking', u'Sewerage Treatment Plant', u'Rain Water Harvesting', u"Children's Play Area", u'Bicycle Track', u'24 Hours Security'], 'price': 6175000, 'Project_Config_No': 27754, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Jun 2016', 'Map_Longitude': u'72.871882000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Dahisar East', 'locality_name': u'Dahisar East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.252242000000000'}, {'Possession': 46, 'Built_Up_Area': 551, 'Project_No': 974, 'amenities': [u'Senior Citizens Corner', u'Tennis Court', u"Children's Play Area", u'Park', u'Malls', u'Landscape Garden', u'Jogging Track', u'Gym', u'Club house', u'Swimming Pool'], 'price': 6000000, 'Project_Config_No': 2539, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Contact Seller For Possession', 'Map_Longitude': u'72.874261000000000', 'No_Of_Bedroom': 1.5, 'Project_Area_Name': u'Dahisar East', 'locality_name': u'Dahisar East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.261703000000000'}, {'Possession': 1049, 'Built_Up_Area': 1070, 'Project_No': 11391, 'amenities': [u'Lifts', u'Rain Water Harvesting', u'Swimming Pool', u'24 Hours Power Backup', u'24 Hours Security', u'Amphitheatre', u"Children's Play Area", u'Club house', u'Garden', u'Gym'], 'price': 11235000, 'Project_Config_No': 46059, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Mar 2019', 'Map_Longitude': u'72.851372000000000', 'No_Of_Bedroom': 2.0, 'Project_Area_Name': u'Borivali West', 'locality_name': u'Borivali West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.251331000000000'}, {'Possession': 137, 'Built_Up_Area': 900, 'Project_No': 1178, 'amenities': [u'Swimming Pool', u'24 Hours Security', u'Amphitheatre', u'Club house', u'Gym', u'Indoor Games', u'Library', u'Lifts', u'Park', u'Party Hall', u'Restaurant', u'Yoga', u'Temple', u'School'], 'price': 7470000, 'Project_Config_No': 33504, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.877657100000000', 'No_Of_Bedroom': 1.5, 'Project_Area_Name': u'Mira Road East', 'locality_name': u'Mira Road East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.267367300000000'}, {'Possession': 229, 'Built_Up_Area': 850, 'Project_No': 18455, 'amenities': [u'Earthquake Resistant', u'Fire Fighting Arrangements', u'Lifts'], 'price': 6120000, 'Project_Config_No': 50174, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2016', 'Map_Longitude': u'72.874557000000000', 'No_Of_Bedroom': 2.0, 'Project_Area_Name': u'Mira Road East', 'locality_name': u'Mira Road East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.271596000000000'}, {'Possession': 76, 'Built_Up_Area': 650, 'Project_No': 17741, 'amenities': [u'Video Door Intercom', u'Security System', u'Solar Water Heating', u'Lifts', u'Earthquake Resistant', u'Gym', u'Intercom'], 'price': 4850000, 'Project_Config_No': 59864, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.885938775500000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Mira Road East', 'locality_name': u'Mira Road East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.272170489000000'}, {'Possession': 76, 'Built_Up_Area': 600, 'Project_No': 17740, 'amenities': [u'Solar Water Heating'], 'price': 4100000, 'Project_Config_No': 59832, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.888870796300000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Mira Road East', 'locality_name': u'Mira Road East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.272286681000000'}, {'Possession': 319, 'Built_Up_Area': 495, 'Project_No': 20015, 'amenities': [u'Earthquake Resistant', u'Intercom', u'Lifts', u'24 Hours Security'], 'price': 6200000, 'Project_Config_No': 53259, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Mar 2017', 'Map_Longitude': u'72.860194084700000', 'No_Of_Bedroom': 0.5, 'Project_Area_Name': u'Dahisar East', 'locality_name': u'Dahisar East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.248849499900000'}, {'Possession': 594, 'Built_Up_Area': 810, 'Project_No': 6465, 'amenities': [u'Club house', u'Parking', u'Fire Fighting Arrangements', u'Gym', u'Jogging Track', u'Lifts', u'Park', u'Rain Water Harvesting', u'Swimming Pool', u"Children's Play Area", u'24 Hours Security'], 'price': 8800000, 'Project_Config_No': 27941, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2017', 'Map_Longitude': u'72.868317000000000', 'No_Of_Bedroom': 1.5, 'Project_Area_Name': u'Dahisar East', 'locality_name': u'Dahisar East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.248323000000000'}, {'Possession': 46, 'Built_Up_Area': 650, 'Project_No': 2324, 'amenities': [u'Rain Water Harvesting', u'Intercom', u"Children's Play Area", u'Garden', u'Gym', u'24 Hours Security'], 'price': 4800000, 'Project_Config_No': 37789, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.881666000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Mira Road East', 'locality_name': u'Mira Road East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.281667000000000'}, {'Possession': 140, 'Built_Up_Area': 935, 'Project_No': 6517, 'amenities': [u'Rain Water Harvesting', u'Parking', u'Lifts', u'Gym', u'Garden', u'24 Hours Security', u"Children's Play Area", u'Fire Fighting Arrangements'], 'price': 11500000, 'Project_Config_No': 27935, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Ready for Possession', 'Map_Longitude': u'72.871844242900000', 'No_Of_Bedroom': 2.0, 'Project_Area_Name': u'Borivali East', 'locality_name': u'Borivali East, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.236363556200000'}, {'Possession': 15, 'Built_Up_Area': 700, 'Project_No': 2232, 'amenities': [u'Club house', u'Skating Rink', u'Squash Court', u'Swimming Pool', u'24 Hours Security', u'Badminton Court', u"Children's Play Area", u'Garden', u'Gym', u'Indoor Games', u'Intercom', u'Jogging Track', u'Lifts', u'Rain Water Harvesting', u'Park', u'Pool Table', u'Tennis Court', u'Wifi Coverage', u'Sewerage Treatment Plant'], 'price': 4900000, 'Project_Config_No': 20308, 'Project_City_Name': u'Mumbai', 'posessionDate': u'May 2016', 'Map_Longitude': u'72.881438200000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Mira Road East', 'locality_name': u'Mira Road East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.283163800000000'}, {'Possession': 168, 'Built_Up_Area': 890, 'Project_No': 7111, 'amenities': [u'Party Hall', u'Vastu Compliant', u'Swimming Pool', u'Rain Water Harvesting', u'Park', u'Parking', u'Lifts', u'Intercom', u'Club house', u'Fire Fighting Arrangements', u'Gym', u'24 Hours Security', u"Children's Play Area"], 'price': 7500000, 'Project_Config_No': 46368, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Oct 2016', 'Map_Longitude': u'72.882871000000000', 'No_Of_Bedroom': 2.0, 'Project_Area_Name': u'Mira Road East', 'locality_name': u'Mira Road East, Beyond Borivali, Mumbai', 'Project_Suburb_Name': u'Beyond Borivali', 'Map_Latitude': u'19.281105000000000'}]
	# print recoPropAttrList
	#recoPropAttrList = [{'Possession': 594, 'Built_Up_Area': 680, 'Project_No': 2236, 'amenities': [u'Club house', u"Children's Play Area", u'24 Hours Security', u'Yoga', u'Tennis Court', u'Swimming Pool', u'Spa', u'Sauna', u'Restaurant', u'Rain Water Harvesting', u'Pool Table', u'Park', u'Lifts', u'Library', u'Landscape Garden', u'Jogging Track', u'Jacuzzi', u'Indoor Games', u'Health Facilities', u'Gym', u'Fire Fighting Arrangements', u'Earthquake Resistant'], 'price': 6460000, 'Project_Config_No': 48213, 'Project_City_Name': u'Mumbai', 'posessionDate': u'Dec 2017', 'Map_Longitude': u'72.827567000000000', 'No_Of_Bedroom': 1.0, 'Project_Area_Name': u'Malad West', 'locality_name': u'Malad West, Ex Western Suburb, Mumbai', 'Project_Suburb_Name': u'Ex Western Suburb', 'Map_Latitude': u'19.194291000000000'}]
	preferanceList = ["budget","location","bhk","possession","amenities"]
	Scoring = scroingSystemForWebsite()
	currTime = time.time()
	Scoring.getScores(searchParams,pastPropAttrList,recoPropAttrList,preferanceList)
	print time.time() - currTime
