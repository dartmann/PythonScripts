'''
Created on 17.10.2014
@author: David Artmann
@version: 0.1
@change: 
@note: script sends structure(groups and tests) about the upcoming reportsuite to the monitoring server.
'''
import httplib, urllib, socket, os, sys, psycopg2.extras, json
#
hostname = socket.gethostname()

jsoncontainer = {}
jsoncontainer["reportname"]=[]
jsoncontainer["report"]=[]
#
sql_conn = "host='localhost' dbname='exam_rmdb' user='postgres' password='Postgre0!'"
try:
    con = psycopg2.connect(sql_conn)
    #Dictcursor because we want to reference the string-names of the columns
    cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #get the latest report(testsuite)
    query = "SELECT r.id id, r.name reportname, g.name groupname, t.name testname, st.name subtestname,\
            r.valuation suiteresult, g.valuation groupresult, t.valuation testresult, st.valuation subtestresult\
            FROM exam_rmdb.report r\
            JOIN exam_rmdb.grp g ON g.report_id = r.id\
            JOIN exam_rmdb.test t ON t.grp_id = g.id\
            JOIN exam_rmdb.subtest st ON st.test_id = t.id\
            WHERE r.id = (SELECT id FROM exam_rmdb.report ORDER BY timelongvalue DESC LIMIT 1);"
    cursor.execute(query)
    latestreport = cursor.fetchall()

    for rows in latestreport:
        jsoncontainer["reportname"]=rows["reportname"]
        jsoncontainer["report"].append({rows["groupname"]:rows["testname"]})
    print jsoncontainer
except psycopg2.DatabaseError, e:
    print "Error %s" % e    
    sys.exit(1)
finally:
    if con:
        cursor.close()
        con.close()
        
#build the json-container
params = urllib.urlencode({"data":jsoncontainer})
#urlencoding is important, because json-format would not be interpreted correctly
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
httpconn = httplib.HTTPConnection("localhost:8080")
#fire the post
##httpconn.request("POST", "/monitoring_server/test/upcomingtest", params, headers)
##response = httpconn.getresponse()
##print response.status, response.reason
##data = response.read()
##print data
httpconn.close()