'''
Created on 16.10.2014
@author:   David Artmann
@version:  0.1
@change:   
@note:     script queries the last report of exam and sends this.
'''
import httplib, urllib, socket, os, sys, psycopg2.extras
#
hostname = socket.gethostname()
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
            WHERE r.id = (SELECT id FROM exam_rmdb.report ORDER BY timelongvalue DESC LIMIT 1)\
            ORDER BY r.timelongvalue DESC LIMIT 1;"
    cursor.execute(query)
    test = cursor.fetchone()
except psycopg2.DatabaseError, e:
    print 'Error %s' % e    
    sys.exit(1)
finally:
    if con:
        cursor.close()
        con.close()
        
#build the json-container
params = urllib.urlencode({"data":{"machine":hostname, "os":os.name, "ip":socket.gethostbyname(hostname), \
                            "id":test['id'], "testname":cTH.server.TestRun.getTestName(), "testresult":test['testresult']}})
#urlencoding is important, because json-format would not be interpreted correctly
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
httpconn = httplib.HTTPConnection("localhost:8080")
#fire the post
httpconn.request("POST", "/monitoring_server/test/tests", params, headers)
response = httpconn.getresponse()
print response.status, response.reason
data = response.read()
print data
httpconn.close()
