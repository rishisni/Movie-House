from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, url_for, redirect, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'

db = SQLAlchemy(app)
db.init_app(app)
app.app_context().push()
login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.init_app(app)


# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

    def __repr__(self):
        return f"<User {self.username}>"


# Admin Model
class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    show = db.relationship('Shows', backref='admin')

    def __repr__(self):
        return f"<Admin {self.username}>"


# Venues Model
class Venues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    place = db.Column(db.String(150))
    location = db.Column(db.String(150), unique=True)
    capacity = db.Column(db.Integer)
    show = db.relationship('Shows', backref='venues')


# Shows Model
class Shows(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    rating = db.Column(db.String(20))
    timing = db.Column(db.String(150))
    venue = db.Column(db.String(150))
    tags = db.Column(db.String(150))
    price = db.Column(db.Integer)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    tickets_booked = db.relationship('Tickets', backref='show')


# Tickets Model
class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timing = db.Column(db.String(150))
    number = db.Column(db.Integer)
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'))


# Routing to index page
@app.route('/')
def index():
    return render_template('index.html')


# Loading User and Admins
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
    return Admin.query.get(int(id))


# Route for Registration Of User
@app.route('/register-user', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists')
            return redirect(url_for('register'))
        new_user = User(email=email, username=username,
                        password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


# Route for Registration Of Admin
@app.route('/register-admin', methods=['GET', 'POST'])
def register_admin():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        admin = Admin.query.filter_by(email=email).first()
        if admin:
            flash('Email already exists')
            return redirect(url_for('register_admin'))
        new_admin = Admin(email=email, username=username,
                          password=generate_password_hash(password, method='sha256'))
        db.session.add(new_admin)
        db.session.commit()
        return redirect(url_for('login_admin'))
    return render_template('register_admin.html')


# Route for Login Of User
@app.route('/login-user', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
        if not user or not check_password_hash(user.password, password):
            flash('Please Check Login details')
            return redirect(url_for('login'))
        return render_template('user_show.html', user=current_user, username=username, password=password)
    return render_template('login.html')


# Route for Login Of Admin
@app.route('/login-admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            login_user(admin)
        if not admin or not check_password_hash(admin.password, password):
            flash('Please Check Login details')
            return redirect(url_for('login_admin'))
        return render_template('home.html', admin=current_user, username=username)
    return render_template('login_admin.html')


# Routing to Home page
@app.route('/home')
@login_required
def home():
    return render_template('home.html')


# Route For Adding new Venue
@app.route('/add-venue', methods=['GET', 'POST'])
@login_required
def add_venue():
    if request.method == "POST":
        venue_name = request.form['name']
        venue_place = request.form['place']
        venue_location = request.form['location']
        venue_capacity = request.form['capacity']
        new_venues = Venues(name=venue_name, place=venue_place,
                            location=venue_location, capacity=venue_capacity)
        db.session.add(new_venues)
        db.session.commit()
        return redirect(url_for('my_venues', admin=current_user, name=venue_name))
    return render_template('add_venue.html', admin=current_user)


# Route For Adding new Shows
@app.route('/add-show', methods=['GET', 'POST'])
@login_required
def add_show():
    venues = Venues.query.all()
    if request.method == "POST":
        show_name = request.form['name']
        show_rating = request.form['rating']
        show_timing = request.form['timing']
        venue_id = request.form['venue']
        show_tags = request.form['tags']
        show_price = request.form['price']
        new_shows = Shows(name=show_name, rating=show_rating, venue_id=venue_id,
                          timing=show_timing, tags=show_tags, price=show_price)
        db.session.add(new_shows)
        db.session.commit()
        return redirect(url_for('my_shows', admin=current_user, venues=venues))
    return render_template('add_show.html', admin=current_user, venues=venues)


# Route For Showing my Venue (Admin)
@app.route('/my_venues')
@login_required
def my_venues():
    venue = Venues.query.all()
    return render_template('my_venues.html', venues=venue, admin=current_user)


# Route For Retriving my Shows(Admin)
@app.route('/my_show')
@login_required
def my_shows():
    show = Shows.query.all()
    return render_template('my_shows.html', shows=show, admin=current_user)



# Route For Retriveing my Shows (User)
@app.route('/user_show')
@login_required
def user_show():
    show = Shows.query.all()
    ticket = Tickets.query.all()
    return render_template('user_show.html', shows=show, user=current_user, tickets=ticket)


# Route To Update my Show
@app.route('/update_show/<int:id>', methods=['POST', 'GET'])
@login_required
def update_show(id):
    show_to_update = Shows.query.get(int(id))
    if request.method == 'POST':
        show_to_update.timing = request.form['timing']
        show_to_update.tags = request.form['tags']
        show_to_update.price = request.form['price']
        db.session.commit()
        flash('Show updated successfully!', 'success')
        return redirect(url_for('my_shows'))
    return render_template('update_show.html', admin=current_user, show=show_to_update)


# Route To Update my Venue
@app.route('/update_venue/<int:id>', methods=['POST', 'GET'])
@login_required
def update_venue(id):
    venue_to_update = Venues.query.get(int(id))
    if request.method == 'POST':
        venue_to_update.capacity = request.form['capacity']
        db.session.commit()
        return redirect(url_for('my_venues'))
    return render_template('update_venue.html', admin=current_user, venue=venue_to_update)


# Route To Delete my Show
@app.route('/delete_show/<int:id>')
@login_required
def delete_show(id):
    show_to_delete = Shows.query.get(id)
    if show_to_delete:
        db.session.delete(show_to_delete)
        db.session.commit()
    return redirect(url_for('my_shows'))


# Route To Delete my Venues
@app.route('/delete_venue/<int:id>')
@login_required
def delete_venue(id):
    venue_to_delete = Venues.query.get(int(id))
    db.session.delete(venue_to_delete)
    db.session.commit()
    # flash("Show deleted Sucessfully")
    return redirect(url_for('my_venues'))


# Route To Book Tickets for Show
@app.route('/book-ticket/<int:id>', methods=['GET', 'POST'])
@login_required
def book_ticket(id):
    show = Shows.query.get(id)
    venue = Venues.query.all()
    if request.method == "POST":
        no_of_seats = request.form['no_of_seats']
        new_ticket = Tickets(user_id=current_user.id, number=no_of_seats,
                             timing=show.timing, price=show.price, show=show)
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for('my_bookings', id=id))
    return render_template('book_ticket.html', user=current_user, show=show)


# Route To Search For Shows , Venues
@app.route('/search')
@login_required
def search():
    query = request.args.get('query')
    venues = Venues.query.filter(Venues.name.ilike(f'%{query}%')).all()
    shows = Shows.query.filter(Shows.name.ilike(f'%{query}%')).all()
    return render_template('search_results.html', query=query, venues=venues, shows=shows)


# Route to Show My Bookings
@app.route('/my_bookings')
@login_required
def my_bookings():
    show = Shows.query.all()
    tickets = Tickets.query.filter_by(user_id=current_user.id).all()
    return render_template('my_bookings.html', tickets=tickets, user=current_user, shows=show)


# Route to Logout User
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=2621)
