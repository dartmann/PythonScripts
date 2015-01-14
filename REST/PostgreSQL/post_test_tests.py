'''
Created on 09.10.2014
@author:      David Artmann
@version:     0.1
@note:        Script queries the report db(exam_rmdb) of exam for the last report(testsuite)\
              and counts all tests in that suite over joins of the related tables.
'''
import httplib, urllib, socket, os, sys, psycopg2.extras
#
hostname = socket.gethostname()
#
sql_conn = "host='localhost' dbname='exam_rmdb' user='postgres' password='Postgre0!'"
try:
    con = psycopg2.connect(sql_conn)
    cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #get the latest report(testsuite)
    query1 = "SELECT id FROM exam_rmdb.report ORDER BY timelongvalue DESC LIMIT 1;"
    cursor.execute(query1)
    latestRep = cursor.fetchone()
    #get all tests with status 'PASS'
    query2 = "SELECT count(*)\
              FROM exam_rmdb.report r\
              JOIN exam_rmdb.grp g ON g.report_id = r.id\
              JOIN exam_rmdb.test t ON t.grp_id = g.id\
              WHERE r.id = %d AND t.valuation = 'PASS';" % (latestRep['id'])
    cursor.execute(query2)
    passedTests = cursor.fetchone()
    #get all tests with status 'FAIL'
    query3 = "SELECT count(*)\
              FROM exam_rmdb.report r\
              JOIN exam_rmdb.grp g ON g.report_id = r.id\
              JOIN exam_rmdb.test t ON t.grp_id = g.id\
              WHERE r.id = %d AND t.valuation = 'FAIL';" % (latestRep['id'])
    cursor.execute(query3)
    failedTests = cursor.fetchone()
    #get all tests with status 'OPEN'
    query4 = "SELECT count(*)\
              FROM exam_rmdb.report r\
              JOIN exam_rmdb.grp g ON g.report_id = r.id\
              JOIN exam_rmdb.test t ON t.grp_id = g.id\
              WHERE r.id = %d AND t.valuation = 'OPEN';" % (latestRep['id'])
    cursor.execute(query4)
    openTests = cursor.fetchone()
    #get all tests with status 'INFO'
    query5 = "SELECT count(*)\
              FROM exam_rmdb.report r\
              JOIN exam_rmdb.grp g ON g.report_id = r.id\
              JOIN exam_rmdb.test t ON t.grp_id = g.id\
              WHERE r.id = %d AND t.valuation = 'INFO';" % (latestRep['id'])
    cursor.execute(query5)
    infoTests = cursor.fetchone()
    #get amount of tests of the last report(testsuite)
    query6 = "SELECT count(*)\
              FROM exam_rmdb.report r\
              JOIN exam_rmdb.grp g ON g.report_id = r.id\
              JOIN exam_rmdb.test t ON t.grp_id = g.id\
              WHERE r.id = %d;" % (latestRep['id'])
    cursor.execute(query6)
    quantityTests = cursor.fetchone()
#   
except psycopg2.DatabaseError, e:
    print 'Error %s' % e    
    sys.exit(1)
finally:
    if con:
        cursor.close()
        con.close()
#build the json-container
params = urllib.urlencode({"data":{"machine":hostname, "os":os.name, "ip":socket.gethostbyname(hostname), \
                             "current":int(latestRep['id']), "skipped":int(openTests[0]), "passed":int(passedTests[0]), \
                             "failed":int(failedTests[0]), "info":int(infoTests[0]), "quantity":int(quantityTests[0])}})
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