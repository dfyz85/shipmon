import pymongo
import logging
from bson.son import SON
import certifi

MONGO_URI = "mongodb://dfyz:rtyfghvbn65@briese-shard-00-00-vryeg.mongodb.net:27017,briese-shard-00-01-vryeg.mongodb.net:27017,briese-shard-00-02-vryeg.mongodb.net:27017/test?ssl=true&replicaSet=briese-shard-0&authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URI,tlsCAFile=certifi.where())
brieseDb = client['shipsBriese']
shipsPossition = brieseDb['shipsPosition']
shipsPossitionNow = brieseDb['shipsPositionNow'] 
vesselsName = brieseDb['shipsData']
countryCode = brieseDb['countryCode']
# Update new BD
# clientLocal = pymongo.MongoClient("mongodb://127.0.0.1:27017/",serverSelectionTimeoutMS=90000)
# brieseDbLocal = clientLocal['shipBrieseBckUp']
# shipsPossitionLocal = brieseDbLocal['shipsPosition'] 

def dbVesselsName():
  pipeline = [
    {"$group":
        {
          "_id": "$imo",
          "vesselName":{"$first":"$vesselName"},
        } 
    },
    {"$sort": SON([("reordingTime", -1)])}
  ]
  db = shipsPossitionNow.aggregate(pipeline)
  #Update new BD
  # db = shipsPossitionLocal.aggregate(pipeline)
  return db

def dbInsertVessel(data,replaceData):
  try:
    shipsPossition.insert_one(data)
  except pymongo.errors.DuplicateKeyError:
     dublicateName = data.get('vesselName')
     logging.info(f'Dublicate {dublicateName}')
  
  # shipsPossitionNow.insert_one(data)
  shipsPossitionNow.replace_one({'imo': replaceData['imo']},replaceData)
  #update empty db
  # shipsPossitionNow.insert_one(data)

def dbInsertNewVessel(data):
  try:
    shipsPossition.insert_one(data)
  except pymongo.errors.DuplicateKeyError:
     dublicateName = data.get('vesselName')
     logging.info(f'Dublicate {dublicateName}')
  #update empty db
  shipsPossitionNow.insert_one(data)

def dbEditShipsData():
  newValues = {
    "$set": {
        "type": "scattergeo",
        "hoverinfo": "text+lon+lat",
        "text": "Current Position",
        "mode": "markers",
        "marker": {"size": 4, "color": "black"}
    }
}
  vesselsName.update_many({},newValues)

def dbGetCountryCode():
  return countryCode.find()
# db = dbVesselsName() 
# for i in db:
#   print(i['count'])