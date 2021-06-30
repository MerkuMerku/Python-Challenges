## Readme 

# setting up venv

set up venv in this repo

run 'py -m pip install -r requirements.txt' on windows to install requirements within your venv

run `py -m pip install --upgrade requests` to upgrade packages

# Running the flask site - PRODUCTION

1) in the flask folder, navigate to the application directory
2) in powershell, run `$env:FLASK_APP = "flasksite.py"` to set the PATH variable for the flask application
3) run `flask run` to start the site

# Running the flask site - DEVELOPMENT

1) in the flask folder, navigate to the application directory
2) in powershell, run `$env:FLASK_APP = "flasksite.py"` to set the PATH variable for the flask application
3) in powershell, run $env:FLASK_ENV = "development" to switch to the development environment
3) run `flask run` to start the site