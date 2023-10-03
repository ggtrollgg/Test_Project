from fastapi import FastAPI
import psycopg2
import psycopg2.extras

import datetime
import requests

app = FastAPI()

def get_Conn():
    hostname = "localhost"
    databasename = "postgres"
    username = "postgres"
    pwd = "1234"
    port_id = "5432"
    try:
        conn = psycopg2.connect(
            host=hostname,
            dbname=databasename,
            user=username,
            password=pwd,
            port=port_id)
    except Exception as error:
        print(error)
        return error
    finally:
        return conn
def getCur(conn):
    cur = None
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        create_script = ''' CREATE TABLE IF NOT EXISTS site(
                                    url varchar(255) PRIMARY KEY,
                                    status varchar(255),
                                    lastchecked varchar(255))'''
        cur.execute(create_script)
        conn.commit()
    except Exception as error:
        print(error)
        return error
    finally:
        return  cur



@app.get("/database")
def test():
    conn = get_Conn()
    cur = getCur(conn)
    # fetch all the data from the table
    cur.execute('SELECT * FROM site')
    # this what printing in separet lines
    result = [{"0": ""}, ]
    for record in cur.fetchall():
        print(record)
        result.append(record)
    result.pop(0)
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()

    return result

@app.get("/database/None-status")
def Get_All_None_status():
    conn = get_Conn()
    cur = getCur(conn)
    cur.execute('''SELECT * FROM site''')

    result = [{"0": ""}, ]
    for record in cur.fetchall():
        if record[1] == None:
            result.append(record)
    result.pop(0)


    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
    return result

@app.get("/database/All-test")
def Get_All_test():
    conn = get_Conn()
    cur = getCur(conn)
    cur.execute('''SELECT * FROM site''')


    result = [{"0": ""}, ]
    for record in cur.fetchall():
        url = (str)(record[0])
        if url.__contains__("test"):
                result.append(record)
    result.pop(0)


    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
    return result

@app.post("/database/Add-url/{url}")
def Add_URL(url: str):
    conn = get_Conn()
    cur = getCur(conn)

    url2 = url.replace("'","/",255)

    insert_script = 'INSERT INTO site  (url,status,lastchecked) VALUES (%s,%s,%s) '
    exists = False
    cur.execute('SELECT * FROM site')
    try:
        for allreadyIn in cur.fetchall():
            if allreadyIn[0] == url2:
                exists = True
        if exists == False:
            cur.execute(insert_script, (url2,None,None))
            conn.commit()
    except Exception as error:
        print(error)
        return "failed"

    return "succuss"

@app.put("/check-status/{url}")
def Update_status_of_url(url: str):
    conn = get_Conn()
    cur = getCur(conn)

    status = Check_status_of_url(url)
    last_checked = datetime.datetime.now()

    Update_Status(conn,cur,url,status,last_checked)

    return {"status: " : status, "last checked: " : last_checked}

def Check_status_of_url(url):
    try:
        status = requests.get(url)
        print("status is: " + (str)(status))
        return status
    except Exception as error:
        print(error)
        return None

def Update_Status (conn,cur,url,status,time_checked):
    update_script = '''update site set status = %s where url = %s '''
    update_record = (status,url)
    cur.execute(update_script, update_record)
    conn.commit()

    update_script = '''update site set lastchecked = %s where url = %s '''
    update_record = (time_checked, url)
    cur.execute(update_script, update_record)
    conn.commit()


