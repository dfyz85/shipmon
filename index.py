import requests
import logging
import argparse
import sys
from os import getlogin
import time
#import brotli
import re
import time
from datetime import datetime
import hashlib

import pandas as pd
from databaseconnection import dbInsertVessel, dbVesselsName, dbGetCountryCode
from const import SHIPS_ID_MARINE, SHIPS_ID_SHIPSINFO
from toolsShipsInfo import getDataShipsInfo, compareTwoDates
def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-d', '--delay', default=0, type=int)
    return parser
#TIME DELAY

user = getlogin()
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')
logging.info(f"Start by {user}.")
#TIME DELAY
parser = createParser()
namespace = parser.parse_args(sys.argv[1:])
#TIME DELAY
#COUNTRY CODE DB DOWNLOAD
data = dbGetCountryCode()
dfCountryCode = pd.DataFrame(data)
#COUNTRY CODE DB DOWNLOAD
vesselsName = dbVesselsName()
shipsId = SHIPS_ID_MARINE
shipsIdInfo = SHIPS_ID_SHIPSINFO
headers = {
            'Host':	'www.marinetraffic.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Connection': 'keep-alive',
            'TE': 'Trailers',
         }
# xxx = {}
# for  i in vesselsName:
#     imo = i['_id']
#     url = 'https://www.marinetraffic.com/en/photos/of/ships/imo:'+imo
#     print(url)
#     headers = {
#             #'Host':	'www.marinetraffic.com',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
#             'Accept': '*/*',
#             #'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
#             #'Accept-Encoding': 'br',
#             #'X-Requested-With': 'XMLHttpRequest',
#             'DNT': '1',
#             'Connection': 'keep-alive',
#             #'Referer': 'Referer: https://www.marinetraffic.com/en/data/?asset_type=vessels&columns=flag,shipname,photo,recognized_next_port,reported_eta,reported_destination,current_port,imo,ship_type,show_on_live_map,time_of_latest_position,lat_of_latest_position,lon_of_latest_position&imo|eq|imo='+str(imo) ,
#             #'Cookie':'__cfduid=d9211ff4bab3ac41408e9cdc110acde951577308491; SERVERID=app5; _ga=GA1.2.1865478285.1577308493; _gid=GA1.2.1372905508.1577308493; _cmpQcif3pcsupported=1; _hjid=7ffc513c-b25d-4461-a959-66ef5a23a55b; hsfirstvisit=; __hstc=153128807.8eec19da8abb58bb97188c619547396b.1577308498600.1577308498600.1577308498600.1; hubspotutk=8eec19da8abb58bb97188c619547396b; __hssrc=1; __hssc=153128807.11.1577308498600; _fbp=fb.1.1577308499503.1875851644; __atuvc=3%7C52; __atuvs=5e03d8bc21bdef7e002; vTo=1; _gat=1',
#             'TE': 'Trailers',
#          }
#     r = requests.get(url, headers = headers).text
#     soup = BeautifulSoup(r,features="lxml")
#     vesselName = soup.find('div',id='gallery').find_all('a')
#     shipID = vesselName[0].get('href').split('shipid:')[1]
#     xxx.update({imo:shipID}) 
# print(xxx)      
for  i in vesselsName:
    try:
        time.sleep(3)
        reordingTime = datetime.now()
        marineTrafficId = shipsId.pop(str(i['_id']))
        imo = i['_id']
        vesselName = str(i['vesselName'])
        mmsi = shipsIdInfo[imo]
        urlPosition = 'https://www.marinetraffic.com/vesselDetails/latestPosition/shipid:'+marineTrafficId
        rPositionShipINfo = getDataShipsInfo(imo, mmsi)
        rPosition = requests.get(urlPosition, headers = headers).json()
        timeStamp = str(datetime.fromtimestamp(rPosition['lastPos']))
        if 'now' in str(timeStamp).lower():
            timeStamp = str(reordingTime)[:-10]
        if compareTwoDates(rPositionShipINfo['time'], timeStamp):
            posittionLat = rPositionShipINfo['posittionLat']
            posittionLon = rPositionShipINfo['posittionLon']
            speed = rPositionShipINfo['speed']
            course = rPositionShipINfo['course']
            timeStamp = rPositionShipINfo['time']
        else:
            posittionLat = rPosition['lat']
            posittionLon = rPosition['lon']
            speed = rPosition['speed']
            course = rPosition['course']
        area = rPosition['areaCode']
        areaName = rPosition['areaName']
        status = rPosition['shipStatus']
        urlDetails = 'https://www.marinetraffic.com/vesselDetails/voyageInfo/shipid:'+marineTrafficId
        rDetails = requests.get(urlDetails, headers = headers).json()
        if rDetails['arrivalPort']:
            countryCodeArrival = str(rDetails['arrivalPort']['countryCode'])
            countryNameArrival = dfCountryCode.loc[dfCountryCode['alpha2'] == countryCodeArrival]['country'].values
            arrival =  f"{rDetails['arrivalPort']['name']} [{str(countryNameArrival[0])}]"
            if rDetails['arrivalPort']['timestamp']:
                eta =  str(datetime.fromtimestamp(rDetails['arrivalPort']['timestamp']))
        if rDetails['departurePort']:
            countryCodeDeparture = str(rDetails['departurePort']['countryCode'])
            countryNameDeparture = dfCountryCode.loc[dfCountryCode['alpha2'] == countryCodeDeparture]['country'].values
            departure =  f"{rDetails['departurePort']['name']} [{str(countryNameDeparture[0])}]"
            if rDetails['departurePort']['timestamp']:
                atd =  str(datetime.fromtimestamp(rDetails['departurePort']['timestamp']))
        if rDetails['draughtReported']:
            draught = round(rDetails['draughtReported'],2)

        # urlInfo = 'https://www.marinetraffic.com/en/vesselDetails/vesselInfo/shipid:'+imo
        # rInfo = requests.get(urlInfo, headers = headers).json()
        # vesselName = rInfo['name']
       
        #print(url)
        #connectTor()
        #TIME DELAY
        time.sleep(namespace.delay)
        #TIME DELAY
        #if vesselName == "BBC ROMANIA":
        #    print(soup.find('div',{'160% line-110'}).attrs) 
        # JS-code data = new Date("2019-07-14 18:30")
        #print(draught)
        #print(vesselName, '\n',timeStamp,'\n', status,'\n',posittionLat,' ',posittionLon,'\n',area)
        myHash = hashlib.md5(vesselName.encode('utf-8')+str(posittionLat).encode('utf-8')+str(posittionLon).encode('utf-8')+str(timeStamp)[:10].encode('utf-8')).hexdigest()
        data = {
            '_id':myHash,
            'vesselName':vesselName,
            'imo':i['_id'],
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
        replaceData = {
            'vesselName':vesselName,
            'imo':i['_id'],
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
        dbInsertVessel(data,replaceData)
    except Exception as e:
        logging.error(f"Open by {user}. Vessels name:{vesselName}", exc_info=True)
logging.info(f"Stop by {user}.")