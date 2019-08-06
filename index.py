import requests
import re
import time
import hashlib
from bs4 import BeautifulSoup
from databaseconnection import dbInsertVessel, dbVesselsName

vesselsName = dbVesselsName()
for  i in vesselsName:
    imo = i['imo']
    url = 'https://www.marinetraffic.com/en/ais/details/ships/imo:'+ imo
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20103103 Firefox/64.0'
    }
    #connectTor()
    time.sleep(10)
    r = requests.get(url, headers = headers).text.encode('utf-8')
    soup = BeautifulSoup(r,features="lxml")
    vesselName = soup.find('h1',{'class':'font-200 no-margin'}).text
    timeStamp = soup.find('div',{'class':'table-cell cell-full collapse-768'}).find('div', {'class':'group-ib'}).find('strong').text.split('(')[0].replace('utc','')
    if 'ago' in timeStamp:
        timeStamp = soup.find('div',{'class':'table-cell cell-full collapse-768'}).find('div', {'class':'group-ib'}).find('strong').text.split('(')[1].replace('utc','')
    # JS-code data = new Date("2019-07-14 18:30")
    tags = soup.find('div',{'class':'table-cell cell-full collapse-768'}).find_all('div', {'class':'vertical-offset-10 group-ib'})
    area = tags[1].text.split('Area:')[1].strip()
    posittionLat = tags[2].find('a', {'class':'details_data_link'}).text.split()[0][:-1]
    posittionLon = tags[2].find('a', {'class':'details_data_link'}).text.split()[2][:-1]
    status = soup.find(text=re.compile("(Moored|Underway Using Engine|Undefined|At Anchor)"))
    print vesselName, '\n',timeStamp,'\n', status,'\n',posittionLat,' ',posittionLon,'\n',area
    myHash = hashlib.md5(vesselName+posittionLat+posittionLon).hexdigest()
    data = {
        '_id':myHash,
        'vesselName':vesselName,
        'time':timeStamp, 
        'status':status, 
        'posittionLat':posittionLat, 
        'posittionLon':posittionLon,
        'area':area
    }
    dbInsertVessel(data)
#Generate .html file
with open('test.html', 'w') as output_file:
  output_file.write(r)
