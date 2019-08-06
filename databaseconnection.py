import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
brieseDb = client['shipsBriese']
shipsPossition = brieseDb['shipsPosition'] 
vesselsName = brieseDb['shipsData']

def dbVesselsName():
  return vesselsName.find()

def dbInsertVessel(data):
  try:
    shipsPossition.insert_one(data)
  except pymongo.errors.DuplicateKeyError:
    print 'Dublicate ', data.get('vesselName')


