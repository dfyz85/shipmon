import pymongo
import pandas as pd
import certifi
import datetime
import sys
from bson.son import SON
from databaseconnection import dbVesselsName

TODAY = datetime.datetime.now()
MONGO_URI = "mongodb://dfyz:rtyfghvbn65@briese-shard-00-00-vryeg.mongodb.net:27017,briese-shard-00-01-vryeg.mongodb.net:27017,briese-shard-00-02-vryeg.mongodb.net:27017/test?ssl=true&replicaSet=briese-shard-0&authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URI,tlsCAFile=certifi.where())
brieseDb = client['shipsBriese']
shipsPossitionNow = brieseDb['shipsPositionNow']
shipsPossition = brieseDb['shipsPosition']
brieseDbBU = client['shipsBrieseBU']
shipsPossitionBU = brieseDbBU['positionVessel']
shipsData = brieseDb['shipsData']
shipsDataBU = brieseDbBU['shipsData']
count = 0 

def setShipsPossitionNow():
    pipeline = [
        {"$group":
            {
            "_id": "$imo",
            "vesselName":{"$first":"$vesselName"},
            "imo": {"$first":"$imo"},
            "time": {"$first":"$time"},  
            "status": {"$first":"$status"}, 
            "posittionLat": {"$first":"$posittionLat"},
            "posittionLon": {"$first":"$posittionLon"},
            "area": {"$first":"$area"},
            "areaName": {"$first":"$areaName"},
            "reordingTime": {"$first":"reordingTime"},
            "speed": {"$first":"$speed"}, 
            "draught": {"$first":"$draught"}, 
            "departure": {"$first":"$departure"}, 
            "arrival": {"$first":"$arrival"},
            "atd": {"$first":"$atd"},
            "eta": {"$first":"$eta"},
            } 
        },
        {"$sort": SON([("reordingTime", -1)])}
    ]
    db = shipsPossition.aggregate(pipeline)
    for item in db:
      shipsPossitionNow.insert_one(item)  
# for item in shipsData.find():
#     shipsDataBU.insert_one(item)
#     count += 1
#     sys.stdout.write(f'Write progress: {count}   \r' )
#     sys.stdout.flush()
# shipsPossitionBU.delete_many({})

def clean_data_colection(data_colection):
    data_colection.delete_many({})
    print(f'{data_colection}colection empty')

def get_backup_file(data_colection,name_db):
    cursor = data_colection.find()
    df =  pd.DataFrame(list(cursor))
    df.to_csv(f'{name_db}_{TODAY}.csv', index=True)

# get_backup_file(shipsPossitionNow,'PossitionNow')
# get_backup_file(shipsPossition, 'Possition')
clean_data_colection(shipsPossition)
# setShipsPossitionNow()