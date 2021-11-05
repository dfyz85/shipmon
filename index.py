import requests
import logging
import argparse
import sys
from os import getlogin
#import brotli
import re
import time
from datetime import datetime
import hashlib
from bs4 import BeautifulSoup
import pandas as pd
from databaseconnection import dbInsertVessel, dbVesselsName, dbGetCountryCode
#TIME DELAY
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
shipsId = {
    '9513622': '365335',
    '9537264': '758448',
    '9513634': '365673',
    '9504724': '365852',
    '9569530': '365385',
    '9415325': '365280',
    '9508421': '366133',
    '9418999': '365089',
    '9436965': '364391',
    '9508407': '152497', 
    '9571399': '366127',
    '9435856': '5579407',
    '9454228': '206287',
    '9578763': '366406',
    '9563744': '366760',
    '9508469': '6036997',
    '9508380': '365195',
    '9256327': '205264',
    '9508471': '366591',
    '9508419': '152612',
    '9362621': '362460',
    '9508457': '366400',
    '9501679': '366455',
    '9504750': '1037050',
    '9347061': '360406',
    '9261994': '366085', 
    '9435026': '363667',
    '9504736': '365858',
    '9301134': '364867', 
    '9297096': '204277', 
    '9435868': '5457938',
    '9357212': '363233',
    '9266308': '361271',
    '9563720': '366536',
    '9571375': '365654',
    '9195420': '205655',
    '9362633': '204335',
    '9468114': '755460',
    '9436331': '364731',
    '9501265': '364716',
    '9508483': '366701',
    '9303314': '363452',
    '9427079': '363211', '9375252': '364517', '9256315': '204901', '9433315': '152782', '9433327': '364165', '9421130': '125683', '9434589': '364815', '9421116': '363291', '9378230': '363557', '9501277': '364720', '9251509': '206340', '9569528': '364979', '9421166': '122987', '9508304': '364952', '9563732': '366543', '9196931': '366099', '9421178': '125906', '9563706': '365848', '9454216': '364435', '9508433': '6037775', '9378242': '363881', '9436953': '363889', '9363508': '205543', '9571387': '366121', '9468102': '758239', '9428205': '365461', '9347059': '359926', '9504798': '366553', '9266310': '361336', '9504786': '366542', '9588598': '755952', '9566796': '206417', '9501681': '366459', '9421142': '125907', '9427081': '363397', '9505302': '3568908', '9386976': '205994', '9501667': '365892', '9504748': '5682360', '9434761': '364269', '9501203': '206156', '9815331': '5707562', '9566784': '365354', '9437153': '364893', '9815329': '5600177', '9700392': '3350145', '9436329': '206229', '9501655': '365884', '9360477': '299843', '9341108': '204134', '9578751': '366521', '9437165': '364895', '9505405': '204265', '9347047': '362806', '9552020': '365615', '9505326': '206420', '9505338': '206271', '9513658': '365684', '9289790': '204946', '9505314': '206386', '9197818': '204431', '9815317': '5396907', '9323651': '205252', '9195470': '205527', '9815343': '5784185', '9434759': '364086', '9281786': '204671', '9386988': '364127', '9195482': '205586', '9434577': '364220', '9505297': '4690815', '9197765': '203867', '9374387': '205623', '9551662': '365606', '9252931': '204537', '9505285': '204182', '9369526': '205665', '9319430': '205378', '9195377': '204416',
    '9570668':'366189',
    '9570670':'366191',
    '9559896':'366409',
    '9559884':'366398',
    '9402043':'363307',
    '9513622':'365335',
    '9570670':'366191',
    '9570668':'366189',
    '9605906':'733368',
    '9593658':'732905',
    '9593684':'732448',
    '9384320':'758267',
    '9430870':'364966',
    '9535307':'725914',
    '9550345':'458718',
    '9431331':'654091',
    '9685097':'376515',
    '9736212':'6280144',
    '9736200':'3350131',
    '9593660':'733213',
    '9605891':'732601',
    '9539389':'690161',
    '9614696':'329679',
    '9614701':'330514',
    }
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
        reordingTime = datetime.now()
        imo = shipsId.pop(str(i['_id']))
        urlPosition = 'https://www.marinetraffic.com/vesselDetails/latestPosition/shipid:'+imo
        rPosition = requests.get(urlPosition, headers = headers).json()
        area = rPosition['areaCode']
        areaName = rPosition['areaName']
        posittionLat = rPosition['lat']
        posittionLon = rPosition['lon']
        status = rPosition['shipStatus']
        speed = rPosition['speed']
        course = rPosition['course']
        timeStamp = str(datetime.fromtimestamp(rPosition['lastPos']))
        if 'now' in str(timeStamp).lower():
            timeStamp = str(reordingTime)[:-10]
        urlDetails = 'https://www.marinetraffic.com/vesselDetails/voyageInfo/shipid:'+imo
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
        vesselName = str(i['vesselName'])
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
        #print(data)
        dbInsertVessel(data,replaceData)
    except Exception as e:
        logging.error(f"Open by {user}. Vessels name:{vesselName}", exc_info=True)
logging.info(f"Stop by {user}.")
#Generate .html file
#with open('test.html', 'w') as output_file:
 # output_file.write(r)
