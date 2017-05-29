import os
from flask import Flask, redirect, url_for, request, render_template, make_response, json, jsonify, g, abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from sqlalchemy.orm import sessionmaker
import requests
import api
from api import *

from db_init import User, Base, Company

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True




engine = create_engine('sqlite:///./test2.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = '/login'


@login_manager.user_loader
def load_user(user_id):
	user = session.query(User).filter(User.id == user_id).first()
	return user


# AUTHENTICATION OF USERS #
###########################


#REGISTER NEW USERS
@app.route('/api/users', methods = ['POST', 'GET'])
def new_user():
	username = request.form['username']
	password = request.form['password']
	email = request.form['email']
	password_confirmation = request.form['confirm-password']

	
	if username == "" or password == "" or email == "":
		return render_template('login.html', message="You need to fill all the fields") #missing arguments

	if password != password_confirmation:
		return render_template('login.html', message="Password confirmation is not equal to password") #password and verify password are not equal
	user = User(username=username, email=email)
	if session.query(User).filter(User.username == username).first() is not None:
		return render_template('login.html', message="That username already exists")
	if session.query(User).filter(User.email == email).first() is not None:
		return render_template('login.html', message="That email is registered with another user")

	user.hash_password(password)
	session.add(user)
	session.commit()
	login_user(user)
	users = session.query(User).all()
	for user in users:
		print(user.username)
		print(user.password)
		print(user.email)

	return redirect(url_for('home'))

#LOGIN EXISTING USER
@app.route('/api/log', methods=["GET", "POST"])
def log():
	username = request.form['username']
	password = request.form['password']
	if username == "" or password == "":
		return render_template('login.html', message="You need to fill all the fields") #missing arguments

	user = session.query(User).filter(User.username == username).first()
	
	if user is not None:
		if user.verify_password(password):
			print("password verified")
			login_user(user)
			flash('Logged in successfully.')
			return redirect(url_for('home'))
		else:
			return render_template('login.html', message="Password is incorrect") #password and verify password are not equal
		
	return render_template('login.html', message="Username doesn't exist")
	 

#PRINT DATA FROM ALL USERS IN THE DATABASES - FOR TEST PURPOSES
@app.route('/allusers')
def all_users():
	users = session.query(User).all()
	for user in users:
		print(user.username)
		print(user.password)
		print(user.email)
	companies = session.query(Company).all()
	for company in companies:
		print(company.name)
		print(company.ticker)
	return "hello"


# API CALLS TO DATABASE #
#########################

@app.route('/api/newcompany/<ticker>')
@login_required
def add_company(ticker):
	par = {
		'identifier': ticker
	}

	data = geturl('companies', par)
	tick = data['ticker']
	name = data['name']
	print(data['ticker'])

	if session.query(Company).filter(Company.user_id == current_user.id).filter(Company.ticker == tick).first() is not None:
		return render_template('add_report.html', message="Company already on your list")
	#ADD COMPANY
	company = Company(name=name, ticker=tick, user_id=current_user.id)
	session.add(company)
	session.commit()
	return redirect(url_for('reports'))


# VIEWS #
#########

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/reports')
@login_required
def reports():
	mycompanies = session.query(Company).filter(Company.user_id == current_user.id).all()
	return render_template('company_list.html', companies=mycompanies)

@app.route('/addreport')
@login_required
def add_report():
	return render_template('add_report.html', message="")

@app.route('/login')
def login():
	return render_template('login.html', message="")

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/home')
@login_required
def home():
	return render_template('dash.html')



# THE REPORT TEMPLATES ARE BELOW:
#################################
#################################

#
@app.route('/rev/<name>')
def revenue(name):
	ticker = name.upper()

	pa = {
		'identifier' : ticker,
		'item' : 'totalrevenue',
		'type' : 'FY',
		'start_date': '2010-01-01',
		'sort_order' : 'asc'
	}

	rev_data = geturl('history', pa)['data']
	c_data = geturl('companies', { 'ticker': ticker})
	
	return render_template('revenue.html', dataset=rev_data, name=c_data)


#Gets a profile of the company
@app.route('/profile/<name>')
def profile(name):
	ticker = name.upper()
	
	params = {
    	'ticker': ticker,
    	'statement': 'income_statement',
    	'type': 'FY'
	}
	financials_dataset = geturl('standardized_financials', params)['data']
	
	c_params = {
    	'identifier': ticker
	}
	companies_dataset = geturl('companies', c_params)
	print(financials_dataset)


	return render_template('company_profile.html', companies_dataset=companies_dataset, financials_dataset=financials_dataset, name=name)



# THE JSON OUTPUTS ARE BELOW HERE
#################################
#################################

@app.route('/json/rev/<name>')
def jsonrev(name):
	ticker = name.upper()

	pa = {
		'identifier' : ticker,
		'item' : 'totalrevenue',
		'type' : 'FY',
		'start_date': '2010-01-01',
		'sort_order' : 'asc'
	}

	rev_data = geturl('history', pa)	

	return jsonify(Data=rev_data)	


@app.route('/json/search/<inputs>')
def search(inputs):
	name = inputs

	par = {
		'conditions' : 'name' + '~contains~' + name
	}

	query = geturl('screener', par)
	print(query)

	return jsonify(results=query)



@app.route('/get/metrics')
def metrics():
	companies = session.query(Company).filter(Company.user_id == current_user.id).all()
	ebitda_margin = {}
	for company in companies:
		par = {
			'identifier' : company.ticker,
			'item': 'ebitdamargin'
		}
		data = geturl('data_point', par)
		ebitda_margin[data['identifier']] = data['value']

	print(EBITDA)

	return "Hello"



if __name__ == '__main__':
	app.run()
