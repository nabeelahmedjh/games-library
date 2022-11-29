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

@app.route('/add-game', methods=['POST', 'GET'])
def addGame():
    if request.method == 'GET':
        return render_template('add_game.html')
    elif request.method == 'POST':
        game_name= request.form['game_name']
        print(game_name)
        qry = "INSERT INTO GLP.game (game_title) VALUES (:1)"
        cur.execute(qry, (game_name,))
        conn.commit()
        return redirect('/')
        # return redirect(url_for('/'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'GET':
        qry = 'SELECT * FROM GLP.game ORDER BY add_at DESC'
        cur.execute(qry)
        data = cur.fetchall()
        context = {
            'data': data
        }
        return render_template('dashboard.html', context=context)


@app.route('/delete-game/<int:pk>', methods=['GET', 'POST'])
def deleteGame(pk):
    if request.method == 'GET':
        return render_template('delete_game.html')
    elif request.method == 'POST':
        qry = 'DELETE FROM GLP.game WHERE game_id = :1'
        cur.execute(qry, [pk])
        conn.commit()
        return redirect('/dashboard')

@app.route('/edit-game/<int:pk>', methods=['GET', 'POST'])
def editGame(pk):
    if request.method == 'GET':
        qry = 'SELECT * FROM GLP.game WHERE game_id=:1'
        cur.execute(qry, [pk])
        data = cur.fetchall()
        context = {
            "data": data
        }
        return render_template('edit_game.html', context=context)
    elif request.method == 'POST':
        qry = "UPDATE GLP.game SET game_title = :1 WHERE game_id = :2"
        updated_data = request.form
        game_title = updated_data['game_title'].lower()
        
        cur.execute(qry, [game_title, pk])
        conn.commit()
        return redirect('/dashboard')

# conn.commit()

# cur.close()
# conn.close()


if __name__ == '__main__':
    app.run()