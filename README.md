# Item Catalog
![Part of the Udacity Front-End Web Development Nanodegree](https://img.shields.io/badge/Udacity-Front--End%20Web%20Developer%20Nanodegree-02b3e4.svg)
A web application that provides a list of items and their information within a variety of categories and integrates third party user registration and authentication. Also includes a JSON API endpoint.

## Usage

### Requirements
Using the Udacity Vagrant VM and the `virtualenv` provided in the repo will cover all requirements/dependencies. Including:
* Virtualenv
* Flask (0.12.1)
* Flask-HTTPAuth (3.2.2)
* Flask-Login (0.4.0)
* Flask-SQLAlchemy (2.2)
* SQLAlchemy (1.1.9)
* httplib2 (0.10.3)
* Jinja2 (2.8)
* oauth2client (4.0.0)
* oauthlib (1.0.3)
* requests-oauthlib (0.8.0)
* Werkzeug (0.12.1)

### Setup external APIs
1. Set up a new Google project [here](https://console.developers.google.com/).
2. Set up Oauth2 under the google API manager.
3. Copy the `CLIENT_ID` and `CLIENT_SECRET` into `config.py`

### Setup virtualenv
1. Ensure virtualenv is installed - [guide](https://virtualenv.pypa.io/en/stable/installation/)
2. Add virtualenv folder for application:
  `$ virtualenv env`
3. Activate virtualenv
  `$ source env/bin/activate`
4. Import requirements
  `$ env/bin/pip3 install -r requirements.txt`

### Run Item Catalog App
1. Navigate to `udacity-fsnd-item-catalog/app`
2. Run with `$ env/bin/python3 run.py`
3. Server will run at `localhost:5000`
4. Optional - populate database with test data:
  * `env/bin/python3 db_seed.py`

### Udacity Vagrant VM
Allows for easy usage with same system configuration used during development:
1. Ensure [Vagrant](https://www.vagrantup.com/), [Virtual Box](https://www.virtualbox.org/) and [Python](https://www.python.org/) are installed on your machine.
2. Clone the Udacity [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm)
3. [Clone](https://github.com/SteadBytes/udacity-fsnd-item-catalog.git) or [download](https://github.com/SteadBytes/udacity-fsnd-item-catalog/archive/master.zip) this repo into the `/vagrant` directory
4. Launch the VM:
  * `vagrant$ vagrant up`
5. SSH into the VM:
  * On Mac/Linux `vagrant$ vagrant ssh`
    * Gives SSH connection details on windows
  * Windows use Putty or similar SSH client
6. In the VM navigate to the `/vagrant/udacity-fsnd-item-catalog` directory:
  * `$ cd /vagrant/udacity-fsnd-item-catalog`
7. Usage is the same as in the [Usage section](#usage)
