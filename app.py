from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template,request,url_for,redirect,flash
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
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
   

class Venues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150),unique=True)
    place =  db.Column(db.String(150))
    location =  db.Column(db.String(150),unique =True)
    capacity = db.Column(db.Integer)
    
    

class Shows(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(150))
    rating = db.Column(db.Integer)
    timing = db.Column(db.String(150))
    venue = db.Column(db.String(150))
    tags = db.Column(db.String(150))
    price = db.Column(db.Integer)
   





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
        if admin:
            flash('Email already exists')
            return redirect(url_for('register'))
        new_admin =Admin(email=email,username = username , password = generate_password_hash(password,method='sha256'))
        db.session.add(new_admin)
        db.session.commit()
        return redirect(url_for('login_admin'))
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
            
        return render_template('home.html',user=current_user,username = username)
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
            
        return render_template('home.html',admin=current_user,username = username )
    return render_template('login_admin.html')


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/add-venue',methods=['GET','POST'])
@login_required
def add_venue():
    if request.method == "POST" :
        name = request.form['name']
        place = request.form['place']
        location = request.form['location']
        capacity = request.form['capacity']
        new_venues = Venues(name=name,place=place,location=location,capacity=capacity)
        db.session.add(new_venues)
        db.session.commit()
        return redirect(url_for('show_venue',admin=current_user,name=name))
    return render_template('add_venue.html',admin=current_user)
    

@app.route('/add-show',methods=['GET','POST'])
@login_required
def add_show():
    if request.method == "POST":
        name= request.form['name']
        rating = request.form['rating']
        timing = request.form['timing']
        venue = request.form['venue']
        tags = request.form['tags']
        price = request.form['price']
        new_shows = Shows(name=name,rating=rating,venue=venue,timing=timing,tags=tags,price=price)
        db.session.add(new_shows)
        db.session.commit()
        return redirect(url_for('show_show',admin=current_user,name=name))
    return render_template('add_show.html',admin=current_user)


@app.route('/show_venue')
@login_required
def show_venue():
    venue = Venues.query.all()
    return render_template('show_venue.html',venues=venue,admin=current_user)

@app.route('/show_show')
@login_required
def show_show():
    show = Shows.query.all()
    return render_template('show_show.html',shows=show,admin=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
   app.run(debug = True,port=2421)

