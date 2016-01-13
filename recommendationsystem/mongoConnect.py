from pymongo import MongoClient

class MongoConnectionForWebsite:

	def __init__(self, url='mongodb://MLadmin:hdfcREDML@ec2-52-35-25-23.us-west-2.compute.amazonaws.com:27017/websiteDataCapture'):
		connection = MongoClient(url)
		db = connection.websiteDataCapture
		self.collection = db.redData


	def getFootprint(self, uniqueCookieId):
		uniqueElement  = "unique_cookie_id"
		print uniqueCookieId
		result = self.collection.find({ uniqueElement : uniqueCookieId, "project_config_no" :{ "$exists": "true" }},{"unique_cookie_id" :1,"project_no" :1,"project_config_no" :1,"tsDate" :1,"element":1 })
		result = result.sort("tsDate",-1)
		propertyArray = []
		result = result.limit(20)
		for post in result:
			print post
			projectNo = post['project_config_no']
			propertyArray.append(int(projectNo))
			print projectNo
			print
		print propertyArray
		return propertyArray




















"""


from pymongo import MongoClient
import time
start_time = time.time()


connection = MongoClient('mongodb://MLUser:ML!5!2pass@10.2.101.76:27017/websiteDataCapture')
db = connection.websiteDataCapture
collection = db.redData
# query = "{ \"unique_cookie_id\" : \"111611011240914ff27\",\"project_no\" : { \"$exists\" : \"true\" } },{\"unique_cookie_id\" :1,\"project_no\" :1,\"tsDate\" :1,\"element\":1 }"
#print query
query = "unique_cookie_id"
ide = "111611011240914ff27"
##  result = collection.find({ "unique_cookie_id" : "111611011240914ff27","project_no" :{ "$exists": "true" }},{"unique_cookie_id" :1,"project_no" :1,"tsDate" :1,"element":1 }).limit(20)

result = collection.find({ query : ide, "project_no" :{ "$exists": "true" }},{"unique_cookie_id" :1,"project_no" :1,"tsDate" :1,"element":1 })
result1 = result.sort("tsDate",-1)
propertyArray = []
result1 = result1.limit(20)
for post in result1:
	print post
	#p1 = str(post)
	#print p1
	projectNo = post['project_no']
	propertyArray.append(int(projectNo))
	print projectNo
	print
	#print "\n"
print result
print

print propertyArray

print("--- %s seconds ---" % (time.time() - start_time))




"""
"""
connection = MongoClient('127.0.0.1', 27017)
db = connection.tes
collection = db.userData
digit = 5
result = collection.find().limit(digit)
for post in result:
	print post
print result
query = "{ \"unique_cookie_id\" : \"111611011240914ff27\",\"project_no\" : { $exists: true } },{\"unique_cookie_id\" :1,\"project_no\" :1,\"tsDate\" :1,\"element\":1 }"
result = collection.find(query).sort({"tsDate" : -1}).limit(20)
print result
for post in result:
	print post
"""