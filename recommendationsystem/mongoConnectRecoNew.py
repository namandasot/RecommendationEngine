from pymongo import MongoClient
from bson.timestamp import Timestamp


class MongoConnectionForWebsite:

    def __init__(self, url='mongodb://MLadmin:hdfcREDML@52.66.177.232:27017/websiteDataCapture'):
        connection = MongoClient(url)
        db = connection.websiteDataCapture
        self.collection = db.redData
        db1 = connection.pastResultData
        self.collection1 = db1.pastData


    def getFootprint(self, uniqueCookieId,date='2016-01-01'):
        uniqueElement = "unique_cookie_id"
        result = self.collection.find({ "data_storage_element" : "project_opened",uniqueElement : uniqueCookieId, "project_config_no" :{ "$exists": "true" },"tsDate":{"$gt": date}},{"unique_cookie_id" :1,"project_config_no" :1,"tsDate" :1 })
        result = result.sort("tsDate",-1)
        propertyArray = []
        result = result.limit(20)
        for post in result:
            projectNo = post['project_config_no']
            try:
                propertyArray.append(int(projectNo))
            except:
                pass
        return propertyArray[:10]
    
    def insertToMongo(self,propList,uniqueCookieId,timeStamp):
        insertDict = {"propList" : propList , "uniqueCookieId":uniqueCookieId,"timeStamp":timeStamp }
        result = self.collection1.insert_one(insertDict)
        return 1
    
    def getFromMongo(self,uniqueCookieId):
        result = self.collection1.find({"uniqueCookieId":uniqueCookieId}).sort("timeStamp",-1).limit(1)
        for a in result:
            print "get From mongo ", a["propList"]
            return a["propList"]
        return []
        






