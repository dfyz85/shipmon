import requests
import logging
import argparse
import sys
from os import getlogin
import re
import time
from datetime import datetime
import hashlib
from bs4 import BeautifulSoup
from databaseconnection import dbInsertVessel, dbVesselsName

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-d', '--delay', default=100, type=int)
    return parser

user = getlogin()
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S')
logging.info(f"Start by {user}.")
parser = createParser()
namespace = parser.parse_args(sys.argv[1:])
vesselsName = dbVesselsName()
for  i in vesselsName:
    try:
        imo = i['imo']
        url = 'https://www.marinetraffic.com/en/ais/details/ships/imo:'+ imo
        #print(url)
        headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20103103 Firefox/64.0'
        }
        #connectTor()
        time.sleep(namespace.delay)
        r = requests.get(url, headers = headers).text.encode('utf-8')
        soup = BeautifulSoup(r,features="lxml")
        vesselName = soup.find('h1',{'class':'font-200 no-margin'}).text
        #if vesselName == "BBC ROMANIA":
        #    print(soup.find('div',{'160% line-110'}).attrs)
        arrival = soup.find('div',{'class':'160% line-110 text-default text-light'})['title']
        departure = soup.find('div',{'160% line-110'})['title']
        timeStamp = soup.find('div',{'class':'table-cell cell-full collapse-768'}).find('div', {'class':'group-ib'}).find('strong').text.split('(')[0].replace('utc','')
        if 'ago' in timeStamp:
            timeStamp = soup.find('div',{'class':'table-cell cell-full collapse-768'}).find('div', {'class':'group-ib'}).find('strong').text.split('(')[1].replace('utc','')
        # JS-code data = new Date("2019-07-14 18:30")
        tags = soup.find('div',{'class':'table-cell cell-full collapse-768'}).find_all('div', {'class':'vertical-offset-10 group-ib'})
        area = tags[1].text.split('Area:')[1].strip()
        posittionLat = tags[2].find('a', {'class':'details_data_link'}).text.split()[0][:-1]
        posittionLon = tags[2].find('a', {'class':'details_data_link'}).text.split()[2][:-1]
        status = soup.find(text=re.compile("(Moored|Underway Using Engine|Undefined|At Anchor)"))
        speedCourse = tags[4].find('strong').text.replace('°','').replace('kn','').replace(' ','').split('/')
        speed = speedCourse[0]
        course = speedCourse[1]
        draughtTag = soup.find('table',{'class':'table table-striped table-striped-alt table-condensed voyage-related table-aftesnippet table-aftesnippet-primary'})
        try:
            draught = draughtTag.find_all('span', {'class':'text-default'})[0].find('b').text.replace('m','')
        except AttributeError:
            draught = None
        #print(draught)
        #print(vesselName, '\n',timeStamp,'\n', status,'\n',posittionLat,' ',posittionLon,'\n',area)
        myHash = hashlib.md5(vesselName.encode('utf-8')+posittionLat.encode('utf-8')+posittionLon.encode('utf-8')).hexdigest()
        reordingTime = datetime.now()
        data = {
            '_id':myHash,
            'vesselName':vesselName,
            'imo':imo,
            'time':timeStamp, 
            'status':status, 
            'posittionLat':posittionLat, 
            'posittionLon':posittionLon,
            'area':area,    
            'reordingTime': str(reordingTime),
            'speed':speed,
            'course':course,
            'draught':draught,
            'departure':departure,
            'arrival':arrival
        }
        dbInsertVessel(data)
    except Exception as e:
        logging.error(f"Open by {user}. Vessels name:{vesselName}", exc_info=True)
logging.info(f"Stop by {user}.")
#Generate .html file
#with open('test.html', 'w') as output_file:
 # output_file.write(r)
