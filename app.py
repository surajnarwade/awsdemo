__author__ = 'spousty'

import psycopg2
from bottle import route, run, get, static_file, DEBUG
import os,json



@route('/')
def index():
    return static_file("index.html", root='./')



@get('/ws/zips')
def getzips():
    results = []
    try:
        conn = psycopg2.connect(database=os.environ.get('DB_NAME'), user=os.environ.get('DB_USER'),
                                host=os.environ.get('DB_HOST'), password=os.environ.get('DB_PASSWORD'))
    except:
        print("couldn't make connection" + os.environ.get('DB_HOST'))

    cur = conn.cursor()
    cur.execute("""select zipcode, count, ST_AsText(the_geom) from zipcodes""")
    rows = cur.fetchall()

    for row in rows:
        result = {}
        result = {'zipcode': row[0], 'count': row[1]}
        coords = []
        temp_coords = row[2]
        lon = temp_coords[temp_coords.find('(')+ 1:temp_coords.find(' ')]
        lat = temp_coords[temp_coords.find(' '):temp_coords.find(')')]
        coords = [lon, lat]
        result['coords'] = coords
        results.append(result)

    return json.dumps({'results': list(results)})

@get('/ws/airports')
def getairports():
    results = []
    try:
        conn = psycopg2.connect(database=os.environ.get('DB_NAME'), user=os.environ.get('DB_USER'),
                                host=os.environ.get('DB_HOST'), password=os.environ.get('DB_PASSWORD'))
    except:
        print(os.environ.get('DB_HOST'))

    cur = conn.cursor()
    cur.execute("""select name, passengers, ST_AsText(the_geom) from airports""")
    rows = cur.fetchall()

    for row in rows:
        result = {}
        result = {'name': row[0], 'passengers': row[1]}
        coords = []
        temp_coords = row[2]
        lon = temp_coords[temp_coords.find('(')+ 1:temp_coords.find(' ')]
        lat = temp_coords[temp_coords.find(' '):temp_coords.find(')')]
        coords = [lon, lat]
        result['coords'] = coords
        results.append(result)

    return json.dumps({'results': list(results)})




#This is for the parkpoints data set which may or may not be there
@get('/db')
def dbexample():
    try:
        conn = psycopg2.connect(database=os.environ.get('DB_NAME'), user=os.environ.get('DB_USER'),
                            host=os.environ.get('DB_HOST'), password=os.environ.get('DB_PASSWORD'))
    except:
        print(os.environ.get('DB_HOST'))

    cur = conn.cursor()
    # cur.execute("""select parkid, name, ST_AsText(the_geom) from parkpoints limit 10""")
    cur.execute("""select parkid, name, ST_AsText(the_geom) from parkpoints ORDER by parkid DESC LIMIT 10""")

    rows = cur.fetchall()
    result_string = "<h2>Here are your results: </h2>"
    for row in rows:
        result_string += "<h3>" + str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + "</h3>"

    cur.close()
    conn.close()

    return result_string




#For Static files

@get("/static/css/<filename:re:.*\.css>")
def css(filename):
    return static_file(filename, root="static/css")

@get("/static/font/<filename:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>")
def font(filename):
    return static_file(filename, root="static/font")

@get("/static/img/<filename:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filename):
    return static_file(filename, root="static/img")

@get("/static/js/<filename:re:.*\.js>")
def js(filename):
    return static_file(filename, root="static/js")


if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True, reloader=True)
