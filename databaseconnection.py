import pymongo
import logging
from bson.son import SON

client = pymongo.MongoClient("mongodb://dfyz:rtyfghvbn65@briese-shard-00-00-vryeg.mongodb.net:27017,briese-shard-00-01-vryeg.mongodb.net:27017,briese-shard-00-02-vryeg.mongodb.net:27017/test?ssl=true&replicaSet=briese-shard-0&authSource=admin&retryWrites=true&w=majority")
brieseDb = client['shipsBriese']
shipsPossition = brieseDb['shipsPosition'] 
vesselsName = brieseDb['shipsData']
# Update new BD
#clientLocal = pymongo.MongoClient("mongodb://127.0.0.1:27017/",serverSelectionTimeoutMS=90000)
#brieseDbLocal = clientLocal['shipBrieseBckUp']
#shipsPossitionLocal = brieseDbLocal['shipsPosition'] 

def dbVesselsName():
  pipeline = [
    {"$group":
        {
          "_id": "$imo",
          "count":SON([("$sum",1)]),
          "vesselName":{"$first":"$vesselName"}
        } 
    },
    {"$sort":SON([("count", 1)])}
  ]
  db = shipsPossition.aggregate(pipeline)
  #Update new BD
  #db = shipsPossitionLocal.aggregate(pipeline)
  return db

def dbInsertVessel(data):
  try:
    shipsPossition.insert_one(data)
  except pymongo.errors.DuplicateKeyError:
     dublicateName = data.get('vesselName')
     logging.info(f'Dublicate {dublicateName}')

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


# db = dbVesselsName() 
# for i in db:
#   print(i['count'])