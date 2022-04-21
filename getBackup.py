import pymongo
import pandas as pd
import certifi
import datetime
import sys

TODAY = datetime.datetime.now()
MONGO_URI = "mongodb://dfyz:rtyfghvbn65@briese-shard-00-00-vryeg.mongodb.net:27017,briese-shard-00-01-vryeg.mongodb.net:27017,briese-shard-00-02-vryeg.mongodb.net:27017/test?ssl=true&replicaSet=briese-shard-0&authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URI,tlsCAFile=certifi.where())
brieseDb = client['shipsBriese']
shipsPossition = brieseDb['shipsPosition']
brieseDbBU = client['shipsBrieseBU']
shipsPossitionBU = brieseDbBU['positionVessel']
shipsData = brieseDb['shipsData']
shipsDataBU = brieseDbBU['shipsData']
count = 0 

shipsDataBU.delete_many({})
print("Ships data BU  empty")

for item in shipsData.find():
    shipsDataBU.insert_one(item)
    count += 1
    sys.stdout.write(f'Write progress: {count}   \r' )
    sys.stdout.flush()
# shipsPossitionBU.delete_many({})

# cursor = shipsPossition.find()
# df =  pd.DataFrame(list(cursor))
# df.to_csv(f'{TODAY}.csv', index=True)


