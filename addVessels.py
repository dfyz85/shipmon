import pymongo
import logging

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
    logging.info('Dublicate ', data.get('vesselName'))
  client.close()

def db_get_vessels():
  client = pymongo.MongoClient("mongodb://localhost:27017/")
  brieseDb = client['shipsBriese']
  shipsPossition = brieseDb['shipsData']
  vessels = shipsPossition.find()
  client.close()
  return vessels
