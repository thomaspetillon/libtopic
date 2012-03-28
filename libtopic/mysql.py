#!/usr/bin/env python
import MySQLdb

class SqlException:
    pass

def execute_non_query(dbname,user,pwd,sql,host='localhost'):
    db = MySQLdb.connect(host=host,db=dbname,passwd=pwd,user=user)
    c = db.cursor()
    c.execute(sql)    
    c.close()
    db.close()

def execute_scalar(dbname,user,pwd,sql,host='localhost'):
    # Open connection
    db = MySQLdb.connect(host=host,db=dbname,passwd=pwd,user=user)
    # Get value
    c = db.cursor()
    c.execute(sql)    
    if (c.rowcount==1):
        row = c.fetchone()
        result = row[0]
    else:
        raise SqlException()
    # Close cursor and connection
    c.close()
    db.close()
    return result

def execute_dataset(dbname,user,pwd,sql,host='localhost'):
    # Open connection
    db = MySQLdb.connect(host=host,db=dbname,passwd=pwd,user=user)
    # Get value
    c = db.cursor()
    c.execute(sql)
    result = []
    for i in range(0,c.rowcount):
        row = c.fetchone()
        result.append(row)            
    # Close cursor and connection
    c.close()
    db.close()
    return result

def get_list(dbname,user,pwd,sql,host='localhost'):
    result = execute_dataset(dbname,user,pwd,sql,host)
    list = []    
    for r in result:
        list.append(str(r[0]))
    return list