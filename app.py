import cx_Oracle
from flask import Flask, redirect, url_for, request, render_template



app = Flask(__name__)

# connection string in the format
# <username>/<password>@<dbHostAddress>:<dbPort>/<dbserviceName>

connectionString = 'system/nabeel123@localhost:1521/xe'

# creating a connection object to connect with connection string data
conn = cx_Oracle.connect(connectionString)

# cursor is used to manipulate database (fetch, delete, select etc)
cur = conn.cursor()


@app.route('/')
def home():
    qry = 'SELECT * FROM GLP.game'
    cur.execute(qry)
    data = cur.fetchall()
    context = {
        'data': data
    }
    return render_template("index.html", context=context)


# conn.commit()

# cur.close()
# conn.close()



if __name__ == '__main__':
    app.run()