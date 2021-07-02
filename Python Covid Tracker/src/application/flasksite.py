from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '3cd81be4c5b6d7ad045dc756c4330b9c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class World(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    total_cases = db.Column(db.Float, nullable=False)
    total_recovered = db.Column(db.Float, nullable=False)
    critical_active = db.Column(db.Float, nullable=False)
    total_deaths = db.Column(db.Float, nullable=False)
    non_critical_active = db.Column(db.Float, nullable=False)
    date_processed = db.Column(db.String(8), nullable=False)
    total_recovered_percentage = db.Column(db.Float, nullable=False)
    critical_active_percentage = db.Column(db.Float, nullable=False)
    total_deaths_percentage = db.Column(db.Float, nullable=False)
    non_critical_active_percentage = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Post('{self.total_cases}', '{self.total_recovered}','{self.critical_active}','{self.total_deaths}','{self.non_critical_active}','{self.date_processed}','{self.total_recovered_percentage}','{self.critical_active_percentage}','{self.total_deaths_percentage}','{self.non_critical_active_percentage}')"


class Continent(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    total_cases = db.Column(db.Float, nullable=False)
    total_recovered = db.Column(db.Float, nullable=False)
    critical_active = db.Column(db.Float, nullable=False)
    total_deaths = db.Column(db.Float, nullable=False)
    non_critical_active = db.Column(db.Float, nullable=False)
    date_processed = db.Column(db.String(8), nullable=False)
    total_recovered_percentage = db.Column(db.Float, nullable=False)
    critical_active_percentage = db.Column(db.Float, nullable=False)
    total_deaths_percentage = db.Column(db.Float, nullable=False)
    non_critical_active_percentage = db.Column(db.Float, nullable=False)
    continent = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Post('{self.total_cases}', '{self.total_recovered}','{self.critical_active}','{self.total_deaths}','{self.non_critical_active}','{self.date_processed}','{self.total_recovered_percentage}','{self.critical_active_percentage}','{self.total_deaths_percentage}','{self.non_critical_active_percentage}','{self.continent}')"


class Country(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    total_cases = db.Column(db.Float)
    total_recovered = db.Column(db.Float)
    critical_active = db.Column(db.Float)
    total_deaths = db.Column(db.Float)
    non_critical_active = db.Column(db.Float)
    date_processed = db.Column(db.String(8))
    total_recovered_percentage = db.Column(db.Float)
    critical_active_percentage = db.Column(db.Float)
    total_deaths_percentage = db.Column(db.Float)
    non_critical_active_percentage = db.Column(db.Float)
    continent = db.Column(db.String(50))
    country = db.Column(db.String(50))

    def __repr__(self):
        return f"Post('{self.total_cases}', '{self.total_recovered}','{self.critical_active}','{self.total_deaths}','{self.non_critical_active}','{self.date_processed}','{self.total_recovered_percentage}','{self.critical_active_percentage}','{self.total_deaths_percentage}','{self.non_critical_active_percentage}','{self.continent}','{self.country}')"


# dummy data
world = [
    {
        'dataname': 'World',
        'TotalCases': 181159470.0,
        'TotalRecovered': 165746400.0,
        'CriticalActive': 80549.0,
        'TotalDeaths': 3924404.0,
        'NonCriticalActive': 11408118.0,
        'TotalRecoveredPerc': 91.49198668452732,
        'CritPerc': 0.044463035308471205,
        'DeathPerc': 2.16627038965978,
        'NonCritPerc': 6.297279338504586
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', world=world)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # dummy login
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('Login successful', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check Username and Password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
