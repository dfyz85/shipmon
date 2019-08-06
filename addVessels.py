import pymongo
def db_connect(data={}):
  client = pymongo.MongoClient("mongodb://localhost:27017/")
  brieseDb = client['shipsBriese']
  shipsPossition = brieseDb['shipsData']
  #data = {
    #'name':'DAXIA',
    #'imo':'9588598'
 #}
  try:
    shipsPossition.insert_one(data)
  except pymongo.errors.DuplicateKeyError:
    print 'Dublicate ', data.get('vesselName')
db_connect()