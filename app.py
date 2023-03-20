from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template,request,url_for,redirect,flash
from flask_login import UserMixin,login_user,LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


app.config['SECRET_KEY' ] ='secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.sqlite3'

db = SQLAlchemy(app)
db.init_app(app) 
app.app_context().push()
login_manager = LoginManager()
login_manager.login_view ='login'
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id =db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20), unique =True)
    email = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(50))
    


class Admin(UserMixin,db.Model):
    id =db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20), unique =True)
    email = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(50))
    


@app.route('/')
def index():
    return render_template('index.html')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@login_manager.user_loader
def load_user(id):
    return Admin.query.get(int(id)) 




@app.route('/register-user',methods=['GET','POST'])
def register():
    if request.method == "POST" :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists')
            return redirect(url_for('register'))
        new_user =User(email=email,username = username , password = generate_password_hash(password,method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/register-admin',methods=['GET','POST'])
def register_admin():
    if request.method == "POST" :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        admin = Admin.query.filter_by(email=email).first()
        if user:
            flash('Email already exists')
            return redirect(url_for('register'))
        new_admin =Admin(email=email,username = username , password = generate_password_hash(password,method='sha256'))
        db.session.add(new_admin)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register_admin.html')


@app.route('/login-user' , methods=['GET','POST'])
def login():
    if request.method == "POST" :
        username =request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
         
        if user and check_password_hash(user.password ,password) :
            login_user(user)
        if not user or not check_password_hash(user.password ,password) :
            flash('Please Check Login details')
            return redirect(url_for('login'))
            
        return render_template('home.html',username = username)
    return render_template('login.html')


@app.route('/login-admin' , methods=['GET','POST'])
def login_admin():
    if request.method == "POST" :
        username =request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
         
        if admin and check_password_hash(admin.password ,password) :
            login_user(admin)
        if not admin or not check_password_hash(admin.password ,password) :
            flash('Please Check Login details')
            return redirect(url_for('login_admin'))
            
        return render_template('home.html',username = username)
    return render_template('login_admin.html')


if __name__ == '__main__':
   app.run(debug = True,port=2301)

