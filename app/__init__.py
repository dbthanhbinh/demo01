from flask import Flask, render_template, request, url_for

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