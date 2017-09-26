from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

from flaskext.mysql import MySQL
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
app.config['MYSQL_DATABASE_DB'] = 'demo01'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def app_home():
    view = 'home/index.html'
    return render_template(view)

@app.route('/users')
def app_users():

    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()

    view = 'users/index.html'
    return render_template(view, datalist=data)

@app.route('/users/add')
def app_add_user():
    view = 'users/add.html'
    return render_template(view)

@app.route('/users/add', methods=['POST'])
def app_doAdd_user():

    try:
        userName = request.form['username']
        userEmail = request.form['email']
        userPass = request.form['password']

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (id, name, email, password, active) VALUE(null, '" + userName + "', '" + userEmail + "', '" + userPass + "',1)")
        conn.commit()

        data = cursor.fetchall()

    except Exception as e:
        return 'Error'
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('app_users'))

@app.route('/users/edit/<int:id>')
def app_edit_user(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s",id)
    data = cursor.fetchone()

    view = 'users/edit.html'
    return render_template(view, objData=data)

@app.route('/users/edit/<int:id>', methods = ['POST'])
def app_doEdit_user(id):
    userName = request.form['username']
    userEmail = request.form['email']

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = %s, email = %s  WHERE id = %s", (userName, userEmail, id))
    conn.commit()

    cursor.close()
    conn.close()
    return redirect (url_for('app_users'))

@app.route('/users/delete/<int:id>', methods = ['GET'])
def app_doDelete_user(id):

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", id)
    conn.commit()

    cursor.close()
    conn.close()
    return redirect (url_for('app_users'))


# API
from flask_restful import Resource, Api

api = Api(app)

class UsersApi(Resource):
    def get(self):
        cursor = mysql.connect().cursor()
        cursor.execute("SELECT * FROM users")
        #data = cursor.fetchall()
        return {'usersList': cursor.fetchall()}

api.add_resource(UsersApi,'/usersapi')