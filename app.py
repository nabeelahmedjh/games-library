import cx_Oracle
from flask import Flask,flash, redirect, url_for, request, render_template, session, g
import base64
from flask_uploads import UploadSet, configure_uploads
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

auth = HTTPBasicAuth()

# connection string in the format
# <username>/<password>@<dbHostAddress>:<dbPort>/<dbserviceName>

connectionString = 'system/nabeel123@localhost:1521/xe'

# creating a connection object to connect with connection string data
conn = cx_Oracle.connect(connectionString)

# cursor is used to manipulate database (fetch, delete, select etc)
cur = conn.cursor()



@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        username = request.form['username']
        password = request.form['password1']
        confirm_password = request.form['password2']
        
        if username and password:
            if password != confirm_password:
                flash("password doesn't match in password and confirm passowrd field")
                return redirect('/register')

            qry = 'SELECT * FROM GLP.users WHERE username= :1'
            
            cur.execute(qry, [username])
            
            found = cur.fetchall()
            
            if len(found) != 0:
                flash("User already exist")
                return redirect('/register')
            
            qry = 'INSERT INTO GLP.users (username, user_type, password) VALUES (:1, :2, :3)'
            
            cur.execute(qry, [username, "regular", password])
            conn.commit()
            flash("Sucessfully registered")
            return redirect('/')
        flash("Username or password doesn't exist")
        return redirect('/register')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        session['user'] = None
        return render_template('login.html')
    else:
        
        username = request.form['username']
        password = request.form['password1']
        qry = 'SELECT username, password, user_type FROM GLP.users WHERE username= :1'
        
        cur.execute(qry, [username])
        
        user = cur.fetchall()
        if len(user) == 0:
            flash("USER DOESN'T EXIST")
            return redirect(url_for("login"))
        
        if password != user[0][1]:
            flash("provided password is wrong")
            return redirect(url_for("login"))

        session['user'] = username
        print(user[0][2])
        session['user_type'] = user[0][2]
        return redirect(url_for("home"))

@app.route('/logout')
def logout():
    session['user'] =  None
    return redirect(url_for('home'))
        
@app.route('/')
def home():

    qry = 'SELECT * FROM GLP.game ORDER BY add_at DESC'
    cur.execute(qry)
    data = cur.fetchall()
    context = {
        'data': data
    }
    return render_template("index.html", context=context)

# @app.route('/add-game', methods=['POST', 'GET'])
# def addGame():
    
#     if 'user' not in session or session['user'] == None or session['user_type'] != 'admin':
#         return redirect(url_for('login'))
        
#     if request.method == 'GET':
       
#         return render_template('add_game.html')
#     elif request.method == 'POST':
#         game_name= request.form['game_name']
#         print(game_name)
#         qry = "INSERT INTO GLP.game (game_title) VALUES (:1)"
#         cur.execute(qry, (game_name,))
#         conn.commit()
#         return redirect('/upload')
#         # return redirect(url_for('/'))

@app.route('/add-game', methods=['POST', 'GET'])
def addGame():
        
    if 'user' not in session:
        return redirect(url_for('login'))


    if request.method == 'POST':
        file = request.files['inputFile']
        data = file.read()
        render_file = render_picture(data)
        name = request.form['name']
        print(render_file)
        qry = "INSERT INTO GLP.game (game_title, game_cover) VALUES (:1, :2)"
        cur.execute(qry, [name, render_file])
        conn.commit()
        return f"success"
        return render_template('upload.html')
    else:
        return render_template('upload_game_image.html')

@app.route('/add-requirements/<int:pk>', methods=["POST", "GET"])
def addRequirements(pk):
    if 'user' not in session or session['user'] == None:
        flash("LOGIN REQUIRED FOR VIEWING DASHBOARD")
        return redirect(url_for('login'))
    if session['user_type'] != 'admin':
        flash("User is not an admin")
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('add_requirements.html')
    else:
        type = request.form.get('type')
        os = request.form.get('os')
        cpu = request.form.get('cpu')
        memory = request.form.get('memory')
        gpu = request.form.get('gpu')
        
        print(type)
        if os == '' or cpu == '' or memory == '' or gpu == '' or type == '':
            flash("Fill all the required columns")
            return redirect('#')
        
        qry = "INSERT INTO GLP.requirements (game_id, req_type, os, cpu, memory, gpu) VALUES (:1, :2, :3, :4, :5, :6)"
        
        cur.execute(qry, [pk, type, os, cpu, memory, gpu])

        conn.commit()
        
        return redirect('')
        

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    
    if 'user' not in session or session['user'] == None:
        flash("LOGIN REQUIRED FOR VIEWING DASHBOARD")
        return redirect(url_for('login'))
    if session['user_type'] != 'admin':
        flash("User is not an admin")
        return redirect(url_for('login'))
    
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


def render_picture(data):

    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic
# conn.commit()

# cur.close()
# conn.close()


if __name__ == '__main__':
    app.run(debug=True)
    app.run()