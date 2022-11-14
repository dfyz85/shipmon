import requests
from os import getlogin
#import brotli
from datetime import datetime
import hashlib
from bs4 import BeautifulSoup
from databaseconnection import dbInsertNewVessel, dbInsertNewDataVessel

VESSEL_NAME = 'BBC MARS'
IMO = 9947770
MARINE_ID = 7166393

def addDataVessel(imo,name):
    data = {
        "_id": imo,
        "name": name,
        "imo": imo,
        "hoverinfo": "text+lon+lat",
        "marker": {
            "size": 4,
            "color": "black"
        },
        "mode": "markers",
        "text": "Current Position",
        "type": "scattergeo",
        "registerLast": "",
        "registerNext": "",
        "registerType": ""
    }
    dbInsertNewDataVessel(data)

def addVessel(imo,id): 
  try:
        reordingTime = datetime.now()
        urlPosition = 'https://www.marinetraffic.com/vesselDetails/latestPosition/shipid:'+id
        urlDetails = 'https://www.marinetraffic.com/vesselDetails/voyageInfo/shipid:'+id
        urlInfo = 'https://www.marinetraffic.com/en/vesselDetails/vesselInfo/shipid:'+id
        #print(url)
        headers = {
            'Host':	'www.marinetraffic.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            #'Accept-Encoding': 'gzip, deflate,',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Connection': 'keep-alive',
            #'Referer': 'https://www.marinetraffic.com/en/ais/details/ships/shipid:365335/vessel:BBC%20LIMA',
            #'Cookie':'_ga=GA1.2.395253674.1437139472; __atuvc=0%7C42%2C26%7C43%2C0%7C44%2C0%7C45%2C10%7C46; __atssc=google%3B17; __hstc=153128807.1e7f97c74a950808d850ae602ebaea4f.1516606452153.1573590744826.1577301361670.25; hubspotutk=1e7f97c74a950808d850ae602ebaea4f; __zlcmid=qchyoos9UHeJXq; __cfduid=d354d627fc06eecbac8ad398ba5a5b16b1560189640; _hjid=59d845fa-caad-43bb-8e30-6ca2bd4c2c89; _fbp=fb.1.1571665909504.2045023531; __gads=ID=59ef9a5d4a2498e6:T=1571755513:S=ALNI_MZbFmVyAZ2zHTEZUXweYDLvsrL-BA; _gaexp=GAX1.2.gqwNE1cuQkmlx_ZHXmcLZg.18279.1; SERVERID=app4; vTo=1; hsfirstvisit=; __hssrc=1; dmxRegion=false; CAKEPHP=3f0o3uctpodu805hit2s0gf3ag; AUTH=EMAIL=pythonsev@gmail.com&CHALLENGE=RQ1pziOwRO489MQIky1e; mt_user[UserID]=2285832; _gid=GA1.2.1262382283.1577301354; _cmpQcif3pcsupported=1; __hssc=153128807.16.1577301361670; _gat=1',
            'TE': 'Trailers',
         }
        #connectTor()
        rPosition = requests.get(urlPosition, headers = headers).json()
        rDetails = requests.get(urlDetails, headers = headers).json()
        rInfo = requests.get(urlInfo, headers = headers).json()
        vesselName = rInfo['name']
        #if vesselName == "BBC ROMANIA":
        #    print(soup.find('div',{'160% line-110'}).attrs) 
        if rDetails['arrivalPort']:
            arrival =  f"{rDetails['arrivalPort']['name']} [{rDetails['arrivalPort']['countryCode']}]"
            if rDetails['arrivalPort']['timestamp']:
                eta =  str(datetime.fromtimestamp(rDetails['arrivalPort']['timestamp']))
        if rDetails['departurePort']:
            departure =  f"{rDetails['departurePort']['name']} [{rDetails['departurePort']['countryCode']}]"
            if rDetails['departurePort']['timestamp']:
                atd =  str(datetime.fromtimestamp(rDetails['departurePort']['timestamp']))     
        timeStamp = str(datetime.fromtimestamp(rPosition['lastPos']))
        if 'ago' or 'now' in str(timeStamp).lower():
            timeStamp = str(reordingTime)[:-10]
        # JS-code data = new Date("2019-07-14 18:30")
        area = rPosition['areaCode']
        areaName = rPosition['areaName']
        posittionLat = rPosition['lat']
        posittionLon = rPosition['lon']
        status = rPosition['shipStatus']
        speed = rPosition['speed']
        course = rPosition['course']
        if rDetails['draughtReported']:
            draught = round(rDetails['draughtReported'],2)
        #print(draught)
        #print(vesselName, '\n',timeStamp,'\n', status,'\n',posittionLat,' ',posittionLon,'\n',area)
        myHash = hashlib.md5(vesselName.encode('utf-8')+str(posittionLat).encode('utf-8')+str(posittionLon).encode('utf-8')+str(timeStamp)[:10].encode('utf-8')).hexdigest()
        data = {
            '_id':myHash,
            'vesselName':vesselName,
            'imo':imo,
            'time':timeStamp, 
            'status':status, 
            'posittionLat':posittionLat, 
            'posittionLon':posittionLon,
            'area':area,
            'areaName':areaName,   
            'reordingTime': str(reordingTime),
            'speed':speed,
            'course':course,
            'draught':draught,
            'departure':departure,
            'arrival':arrival,
            'atd':atd,
            'eta':eta
        }
        #print(data)
        dbInsertNewVessel(data)
  except Exception as e:
    print(e)
addDataVessel(str(IMO),VESSEL_NAME)
addVessel(str(IMO),str(MARINE_ID))