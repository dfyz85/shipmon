import requests
from bs4 import BeautifulSoup
import re

# '2022-04-18 14:36:27 UTC, 1.18875, 103.955, course: 71, speed: 0'
def getArrayFromData(text):
    return [re.sub('[a-zA-Z]', '', s).strip() for s in text.split(',')]

def compareTwoDates(date1, date2):
    date1ar = date1.split(' ')
    date2ar = date2.split(' ')
    if date1ar[0].replace('-','') > date2ar[0].replace('-',''):
        return True
    elif date1ar[0].replace('-','') == date2ar[0].replace('-',''):
        return True if date1ar[1].replace(':','') > date2ar[1].replace(':','') else False
    else:
        return False  
    
def getDataShipsInfo(imo, mmsi):
    try:
        headersShipsInfo = {
                'Host':	'www.shipinfo.net',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
                'Accept': '*/*',
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                'X-Requested-With': 'XMLHttpRequest',
                'DNT': '1',
                'Connection': 'keep-alive',
                'TE': 'Trailers',
            }
        urlPositionInfo = f'https://shipinfo.net/find_vessel_noname_vessel_IMO-{imo}_MMSI-{mmsi}'
        rPositionInfo = requests.get(urlPositionInfo, headers = headersShipsInfo).text
        soup = BeautifulSoup(rPositionInfo,features="lxml")
        vesselPositionShipInfo = soup.find("div", {"class": "extra"}).b.getText()
        dataArray = getArrayFromData(vesselPositionShipInfo)
        dataDict = {
            'time':dataArray[0], 
            'posittionLat':dataArray[1], 
            'posittionLon':dataArray[2],
            'speed':dataArray[4],
            'course':dataArray[3], 
        }
        return dataDict
    except Exception as e:
        return {
            'time':'', 
            'posittionLat':'', 
            'posittionLon':'',
            'speed':'',
            'course':'', 
        }
    # print(urlPositionInfo, vesselPositionShipInfo)
    
    