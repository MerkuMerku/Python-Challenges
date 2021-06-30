from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '3cd81be4c5b6d7ad045dc756c4330b9c'

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


@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
