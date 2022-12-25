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


@app.route('/favorites/<int:pk>', methods=["POST", "GET"])
def favorites(pk):
    
    if 'user' not in session or session['user'] == None:
        flash("LOGIN REQUIRED FOR ADDING GAME INTO FAVORITES")
        return redirect(url_for('login'))

    qry = 'SELECT user_id FROM GLP.users WHERE username = :1'
    cur.execute(qry, [session['user']])
    user_id = cur.fetchall()[0][0]
    
    if request.method == "GET":
        
        qry = "SELECT * FROM GLP.game LEFT OUTER JOIN GLP.favorites ON GLP.game.game_id = GLP.favorites.game_id WHERE GLP.favorites.user_id = :1"
        cur.execute(qry, [user_id])
        data = cur.fetchall()
        context = {
            'data': data
        }
        return render_template("favorites.html", context=context)
    else:   
        qry = 'SELECT * FROM GLP.favorites WHERE user_id = :1 AND game_id = :2'
        cur.execute(qry, [user_id, pk])
        res = cur.fetchall()
        if len(res) != 0:
            flash("ALREADY ADDED TO THE FAVOTIES GALLERY")
            return redirect(f'/game/{pk}')
        qry = "INSERT INTO GLP.favorites VALUES (:1, :2)";
        cur.execute(qry, [pk, user_id])
        conn.commit()
        flash("SUCCESSFULLY ADDED TO THE FAVOTIES GALLERY")
        return redirect(f'/game/{pk}')
        


@app.route('/game/<int:pk>', methods=["POST", "GET"])
def game(pk):
    
    qry = "SELECT * FROM GLP.game WHERE game_id = :1"
    cur.execute(qry, [pk])
    game_details = cur.fetchall()
    
    qry = "SELECT GLP.genre.genre_id, GLP.genre.genre_name, GLP.genre.genre_description FROM GLP.genre LEFT OUTER JOIN GLP.has_genres ON GLP.genre.genre_id = GLP.has_genres.genre_id WHERE GLP.has_genres.game_id = :1";
    cur.execute(qry, [pk])
    game_genres = cur.fetchall()
    
    qry = "SELECT * FROM GLP.requirements WHERE game_id = :1"
    cur.execute(qry, [pk])
    game_requirements = cur.fetchall()
    
    context = {
        'game_details': game_details,
        'game_genres': game_genres,
        'game_requirements': game_requirements
    }
    
    return render_template('game.html', context=context)


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
        
        game_desc = request.form['game_desc']
        qry = "INSERT INTO GLP.game (game_title, game_cover, game_desc) VALUES (:1, :2, :3)"
        cur.execute(qry, [name, render_file, game_desc])
        conn.commit()
        qry = "SELECT game_id FROM GLP.game WHERE game_title = :1"
        cur.execute(qry, [name])
        id = cur.fetchall()
        
        return redirect(f"/add-requirements/{id[0][0]}")
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
        type = 'minimum'
        os = request.form.get('min_os')
        cpu = request.form.get('min_cpu')
        memory = request.form.get('min_memory')
        gpu = request.form.get('min_gpu')
        
        if os == '' or cpu == '' or memory == '' or gpu == '' or type == '':
            flash("Fill all the required columns")
            return redirect('#')
        
        qry = "INSERT INTO GLP.requirements (game_id, req_type, os, cpu, memory, gpu) VALUES (:1, :2, :3, :4, :5, :6)"
        
        cur.execute(qry, [pk, type, os, cpu, memory, gpu])
        
        type = 'recommended'
        os = request.form.get('max_os')
        cpu = request.form.get('max_cpu')
        memory = request.form.get('max_memory')
        gpu = request.form.get('max_gpu')
        
        if os == '' or cpu == '' or memory == '' or gpu == '' or type == '':
            flash("Fill all the required columns")
            return redirect('#')
        
        qry = "INSERT INTO GLP.requirements (game_id, req_type, os, cpu, memory, gpu) VALUES (:1, :2, :3, :4, :5, :6)"
        
        cur.execute(qry, [pk, type, os, cpu, memory, gpu])

        conn.commit()
        
        return redirect(f'/add-details/{pk}')

@app.route('/add-details/<int:pk>', methods=["POST", "GET"])
def addDetails(pk):
    
    if 'user' not in session or session['user'] == None:
        flash("LOGIN REQUIRED FOR VIEWING DASHBOARD")
        return redirect(url_for('login'))
    if session['user_type'] != 'admin':
        flash("User is not an admin")
        return redirect(url_for('login'))

    if request.method == 'GET':
        qry = 'SELECT * FROM GLP.genre'
        
        cur.execute(qry)
        
        genres = cur.fetchall()
        
        context = {
            "genres": genres
        }
        
        
        print(genres)
        return render_template('add_details.html', context=context)
    else:
        release_date = request.form.get("releaseDate")
        download_link = request.form.get("downloadLink")
        rating = int(request.form.get("rating"))
        print(release_date)
        
        qry = "UPDATE GLP.game SET release_date = to_date(:1, 'yyyy-mm-dd'), download_link = :2, rating = :3 WHERE game_id = :4"
        cur.execute(qry, [release_date, download_link, rating, pk])
        conn.commit()
        for i in range(17):
            print(request.form.get(f"{i}"))
            if request.form.get(f"{i}") != None:
                qry = "INSERT INTO GLP.has_genres VALUES (:1, :2)"
                cur.execute(qry, [pk, i])
                conn.commit()
        return redirect("/")

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
        qry = 'DELETE FROM GLP.requirements WHERE game_id = :1'
        cur.execute(qry, [pk])
        conn.commit()
        
        qry = 'DELETE FROM GLP.has_genres WHERE game_id = :1'
        cur.execute(qry, [pk])
        conn.commit()
        
        qry = 'DELETE FROM GLP.game WHERE game_id = :1'
        cur.execute(qry, [pk])
        conn.commit()
        return redirect('/dashboard')


@app.route('/edit-game/<int:pk>', methods=['GET', 'POST'])
def editGame(pk):
    if request.method == 'GET':
        qry = "SELECT * FROM GLP.game WHERE game_id = :1"
        cur.execute(qry, [pk])
        game_details = cur.fetchall()
        
        qry = "SELECT GLP.genre.genre_id, GLP.genre.genre_name, GLP.genre.genre_description FROM GLP.genre LEFT OUTER JOIN GLP.has_genres ON GLP.genre.genre_id = GLP.has_genres.genre_id WHERE GLP.has_genres.game_id = :1";
        cur.execute(qry, [pk])
        game_genres = cur.fetchall()
        
        qry = "SELECT * FROM GLP.requirements WHERE game_id = :1"
        cur.execute(qry, [pk])
        game_requirements = cur.fetchall()
        
        context = {
            'game_details': game_details,
            'game_genres': game_genres,
            'game_requirements': game_requirements
        }
        
        return render_template('edit_game.html', context=context)
    elif request.method == 'POST':
        
        # updating minimun req
        os = request.form.get('min_os')
        cpu = request.form.get('min_cpu')
        memory = request.form.get('min_memory')
        gpu = request.form.get('min_gpu')
        
        qry="UPDATE GLP.requirements SET os = :1, cpu = :2, memory = :3, gpu = :4 WHERE game_id = :5 AND req_type = 'minimum'"
        cur.execute(qry, [os, cpu, memory, gpu, pk])
        conn.commit()
        
        # updating recommended req
        os = request.form.get('max_os')
        cpu = request.form.get('max_cpu')
        memory = request.form.get('max_memory')
        gpu = request.form.get('max_gpu')
        
        qry="UPDATE GLP.requirements SET os = :1, cpu = :2, memory = :3, gpu = :4 WHERE game_id = :5 AND req_type = 'recommended'"
        cur.execute(qry, [os, cpu, memory, gpu, pk])
        conn.commit()
        
        game_title = request.form.get('game_name').lower()
        game_desc = request.form.get('game_desc').lower()
        rating = request.form.get('rating')
        download_link = request.form.get('download_link')
        
        qry = "UPDATE GLP.game SET game_title = :1, game_DESC = :2, download_link = :3, rating = :4 WHERE game_id = :5"
        cur.execute(qry, [game_title, game_desc, download_link, rating, pk])
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