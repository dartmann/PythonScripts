'''
Created on 09.10.2014

@author: daartman
@attention: script doesn't work, because of the json formatted string, urlencoded works
'''
import httplib
body = r'{"jsondatastr":["data"],"name":["Name des PCs"],"os":["OS des PCs"],"ip":["IP des PCs"]}'
print body
headers = {"Content-type": "application/json", "Accept": "text/plain"}
conn = httplib.HTTPConnection("localhost:8080")
conn.request("POST", "/monitoring_server/machines", body, headers)
response = conn.getresponse()
print response.status, response.reason
data = response.read()
print data
conn.close()