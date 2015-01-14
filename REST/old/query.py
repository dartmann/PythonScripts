'''
Created on 10.10.2014

@author: David Artmann
'''
import psycopg2, sys, pprint, psycopg2.extras

conn_string = "host='localhost' dbname='exam_rmdb' user='postgres' password='Postgre0!'"

try:
    con = psycopg2.connect(conn_string)
    cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT count(*) FROM exam_rmdb.project p \
                  JOIN exam_rmdb.report r ON r.project_id = p.id \
                  JOIN exam_rmdb.grp g ON g.report_id = r.id \
                  JOIN exam_rmdb.test t ON t.grp_id = g.id \
                  JOIN exam_rmdb.subtest st ON st.test_id = t.id \
                  WHERE t.valuation = 'FAIL';")
    ver = cursor.fetchone()
    print ver[0]
    

except psycopg2.DatabaseError, e:
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    if con:
        cursor.close()
        con.close()