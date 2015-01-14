'''
Created on 08.10.2014

@author: daartman
'''
import requests, json

url = "http://localhost:8080/monitoring_server/machines"
data=json.dumps({"data": {"name":"Name des PCs", "os":"OS des PCs", "ip":"IP des PCs"}})
print data

#payload = {"cluster":"System X", "machine":"Computer X"}

headers = {"content-type": "application/x-www-form-urlencoded", "accept": "text/plain"}
r = requests.post(url, params=data, headers=headers)
print r.status_code, r.reason, "\n", r.headers, "\n", r.text, "\n"