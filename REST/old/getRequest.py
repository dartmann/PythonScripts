'''
Created on 06.10.2014

@author: daartman

@attention: only needed if going through proxy:

proxy_ip = "10.151.249.76:8080"
proxy_support = urllib2.ProxyHandler({"http":proxy_ip})
opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
urllib2.install_opener(opener)
'''
import httplib, urllib

conn = httplib.HTTPConnection("localhost:8080")
conn.request("GET", "/monitoring_server/alarm")
response =  conn.getresponse()
print response.status, response.reason
data1 = response.read()
print data1
conn.close()