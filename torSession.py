import requests
from subprocess import Popen as terminal

stopTor = ['cmd', '/K', 'taskkill', '/im', 'tor.exe', '/t', '/f']
startTor = ['cmd', '/K', 'tor']

terminal(startTor)
#print(startPID.pid)
#stopCMD = ['cmd', '/K', 'taskkill', '/im', str(startPID.pid), '/t', '/f']
#terminal(stopCMD)
print("Start TOR")
session = requests.session()
session.proxies = {}
session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'
r = session.get('http://httpbin.org/ip')
print(r.text)

terminal(stopTor)
#terminal(stopTor, shell=True) if you need terminal window
session.proxies['http'] = ''
session.proxies['https'] = ''
r = session.get('http://httpbin.org/ip')
print(r.text)