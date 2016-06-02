from pymongo import MongoClient


class MongoConnectionForWebsite:

    def __init__(self, url='mongodb://MLadmin:hdfcREDML@ec2-52-35-25-23.us-west-2.compute.amazonaws.com:27017/websiteDataCapture'):
        connection = MongoClient(url)
        db = connection.websiteDataCapture
        self.collection = db.redData


    def getFootprint(self, uniqueCookieId,date):
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
        return propertyArray





