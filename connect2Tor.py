import socket
import socks
import requests

def connectTor():
   socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050, True)
   socket.socket = socks.socksocket
connectTor()
print 'Connect to Tor'
url = 'https://www.marinetraffic.com/en/ais/details/ships/imo:9435868'
headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20103103 Firefox/64.0'
}
r = requests.get(url, headers = headers).text.encode('utf-8')
print r