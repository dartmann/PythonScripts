'''
Created on 08.10.2014

@author: David Artmann 
'''
import requests

url = "http://localhost:8080/monitoring_server/alarm"
header = {"content-type":"application/json",  "accept":"text/plain"}
r = requests.get(url, params=header)
print r.url
print r.status_code, r.reason