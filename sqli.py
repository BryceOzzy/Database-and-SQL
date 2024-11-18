#!/usr/bin/python3

from flask import Flask, render_template, request
import mysql.connector, os
import json
with open('/home/bryce/databaseExample/09-1-connectToDB/secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCredentials']



app = Flask(__name__)


@app.route('/', methods=['GET'])
def showTable():
    """This is vulnerable to the following SQL injection:
    http://localhost:8000/?id=1' or 1=1 --%20"""
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    id = request.args.get('id')

    # Fetch the value from the table with a matching ID
    sqlstring = "Select * from actor where actor_id=%s" #changed to parameterized query with %s
    print(sqlstring)
    mycursor.execute(sqlstring, (id,)) #Passed the id parameter as a tuple to execute
    myresult = mycursor.fetchall()
    mycursor.close()
    connection.close()
    output = "<br />\n".join([str(row) for row in myresult])
    return output


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")