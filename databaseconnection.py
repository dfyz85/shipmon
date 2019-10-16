import pymongo
client = pymongo.MongoClient("mongodb://dfyz:rtyfghvbn65@briese-shard-00-00-vryeg.mongodb.net:27017,briese-shard-00-01-vryeg.mongodb.net:27017,briese-shard-00-02-vryeg.mongodb.net:27017/test?ssl=true&replicaSet=briese-shard-0&authSource=admin&retryWrites=true&w=majority")
brieseDb = client['shipsBriese']
shipsPossition = brieseDb['shipsPosition'] 
vesselsName = brieseDb['shipsData']

def dbVesselsName():

  return vesselsName.find(no_cursor_timeout=True)

def dbInsertVessel(data):
  try:
    shipsPossition.insert_one(data)
  except pymongo.errors.DuplicateKeyError:
    print ('Dublicate ', data.get('vesselName'))


