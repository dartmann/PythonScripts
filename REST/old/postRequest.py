'''
Created on 08.10.2014

@author: daartman

@attention: only needed if going through proxy:

proxy_ip = "10.151.249.76:8080"
proxy_support = urllib2.ProxyHandler({"http":proxy_ip})
opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
urllib2.install_opener(opener)
'''
import httplib, urllib

paramspart = {"name": "Test PC",
              "os": "Windows 7",
              "ip": "192.168.2.20"}
params = urllib.urlencode({"data":paramspart})
print params
#funktioniert nur, weil die formatierung nicht auf json steht:
header = {"Content-type": "application/x-www-form-urlencoded",
          "Accept": "text/plain"}
conn = httplib.HTTPConnection("localhost:8080")
conn.request("POST", "/monitoring_server/machines", params, header)
response = conn.getresponse()
print response.status, response.reason
data = response.read()
print data
conn.close()

