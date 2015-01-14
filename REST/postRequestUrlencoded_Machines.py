'''
Created on 09.10.2014

@author: David Artmann
@attention: only works with urlencoding, json format woun't work.
'''
import httplib, urllib, socket, os, psycopg2, sys, pprint, psycopg2.extras

hostname = socket.gethostname()
params = urllib.urlencode({"data": {"name":hostname, "os":os.name, "ip":socket.gethostbyname(hostname)}})
print params
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
httpconn = httplib.HTTPConnection("localhost:8080")
##httpconn.request("POST", "/monitoring_server/machines", params, headers)
##response = httpconn.getresponse()
##print response.status, response.reason
##data = response.read()
##print data
httpconn.close()