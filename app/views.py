from flask import render_template, flash, redirect, session, g, jsonify, request
from app import app
from .forms import LoginForm
from .forms import FilterForm
from .forms import DeliveryForm
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from app import db,models
import v2
import vk

@app.route('/')
@app.route('/index')
def index():

	form = LoginForm()
	return render_template('login.html', form = form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		session ['user_login'] =form.login.data
		session ['user_password']=form.password.data

		auth1 = v2.VKAuth(email = session.get('user_login'),pswd = session.get('user_password'))
		auth1.auth()
		session ['at'] = auth1.get_token()
		session1 = vk.Session(access_token=session.get('at'))
		api = vk.API(session1)
	return redirect('/search')


@app.route('/search', methods = ['GET', 'POST'])
def search():
	try:
		session1 = vk.Session(access_token=session.get('at'))
	except:
		return redirect ('/login')
	api = vk.API(session1)
	form = FilterForm()

	UA_CID = api.database.getCountries(code='UA')[0]['cid']
	CITY = api.database.getCities(country_id= UA_CID, q= form.city.data)
	nc = 0
	CITY_ID = CITY[nc]['cid']
	age_from = form.age_from.data
	age_to = form.age_to.data
	school_year=form.school_year.data
	school_num = form.school.data
	SCHOOL =  api.database.getSchools(q=school_num,city_id=CITY_ID)
	SCHOOL_ID = SCHOOL[1]['id']
	name=form.name.data

	users = api.users.search(count=25 ,q =name,city=CITY_ID, country=UA_CID, age_from=age_from, age_to=age_to, school_year=school_year,school = SCHOOL_ID,  fields = "photo_100,last_seen,photo_id,has_mobile,universities,can_write_private_message,can_send_friend_request")
	for u in users:
		try:
			if u['universities']:
				print(u['universities'][0]['name'])
		except :
			pass

	return render_template('search.html', title = 'Search', users= users, form = form)


@app.route('/delivery', methods = ['GET', 'POST'])
def delivery():
	name = "test"
	delivery = "test"
	form = DeliveryForm()
	if form.validate_on_submit():
		db.create_all()
		delivery = form.text.data
		name = form.name.data
		text1 = models.User(nickname= delivery, id=name)
		db.session.add(text1)
		db.session.commit()
		deliv = models.User.query.filter_by(id=name).first()
		session ['del']= form.text.data #deliv
		print (delivery)
		return render_template('delivery.html', form = form,text1=text1,delivery=delivery,name=name,deliv=deliv)
	else:
		return render_template('delivery.html', form=form)

@app.route ('/message', methods = ['GET', 'POST'],)
def message():
	session1 = vk.Session(access_token=session.get('at'))
	api = vk.API(session1)
	id = request.args.get('id')
	ud = api.users.get(user_ids=id,fields='last_seen,photo_id,has_mobile,universities,can_write_private_message,can_send_friend_request')[0]
	print (id)
	print(ud)
	if ud['can_write_private_message']== 1:
		api.messages.send(user_id=id, message= session.get('del').replace('%user_name%', ud['first_name']))
	elif ud['can_send_friend_request']== 1:
		api.friends.add(user_id=id, text='Hi')
	return redirect('/search')


@app.route('/logout', methods = ['GET', 'POST'])
def logout():
	session.clear()
	return redirect('/')






