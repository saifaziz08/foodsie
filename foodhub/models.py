from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import time

db = SQLAlchemy()

class Users(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100), nullable=True)
  lastname = db.Column(db.String(100), nullable=True)
  code = db.Column(db.String(5), nullable=True)
  email = db.Column(db.String(120), unique=True, nullable=True)
  points = db.Column(db.Integer, nullable=True)
  pwdhash = db.Column(db.String(54), nullable=True)
  def __init__(self, firstname=None, lastname=None, email=None, password=None, points=0, card_hash=None):
  	if not card_hash:
	    self.firstname = firstname.title()
	    self.lastname = lastname.title()
	    self.email = email.lower()
	    self.points = points
	    self.set_password(password)
	else:
		self.card_hash = card_hash
  def set_password(self, password):
  	self.pwdhash = generate_password_hash(password)

  def check_password(self, password):
  	return check_password_hash(self.pwdhash, password)

class Restaurants(db.Model):
	__tablename__ = 'restaurants'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	description = db.Column(db.String(255))
	food_type = db.Column(db.String(100))
	email = db.Column(db.String(120), unique=True)
	pwdhash = db.Column(db.String(54))
	image = db.Column(db.String(255), nullable=True)
	postal_code = db.Column(db.String(10))
	address = db.Column(db.String(255))

	def __init__(self, name, description, food_type, email, password, postal_code, address, image=''):
		self.name=name
		self,lastname=lastname.title()
		self.firstname=firstname.title()
		self.email=email.lower()
		self.set_password(password)
		self.description = description
		self.food_type = food_type
		self.image = image
		self.postal_code = postal_code
		self.address = address
	def set_password(self, password):
	  	self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
	  	return check_password_hash(self.pwdhash, password)

class MenuItems(db.Model):
	__tablename__ = 'menu_items'
	id = db.Column(db.Integer, primary_key = True)
	restaurant_id = db.Column(db.Integer, db.ForeignKey(Restaurants.id))
	name = db.Column(db.String(100))
	description = db.Column(db.String(255))
	category = db.Column(db.String(80))
	price = db.Column(db.Integer)

	def __init__(self, restaurant_id, name, description, category, price):
		self.name = name
		self.description = description
		self.category = category
		self.price = price

class Feedback(db.Model):
	__tablename__ = 'feedback'
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'), nullable=True)
	restaurant_id = db.Column(db.Integer, db.ForeignKey(Restaurants.id, ondelete='CASCADE'))
	item_id = db.Column(db.Integer, db.ForeignKey(MenuItems.id, ondelete='CASCADE'), nullable=True)
	rating = db.Column(db.Integer)
	note = db.Column(db.String(140), nullable = True)
	created_at_millis = db.Column(db.BIGINT, nullable=True)
	completed = db.Column(db.Integer, default=0)

	def __init__(restaurant_id, item_id, user_id):
		self.restaurant_id = restaurant_id
		self.item_id = item_id
		self.user_id = user_id
		self.created_at_millis = int(time.time()*1000)


class Announcements(db.Model):
	__tablename__ = 'announcements'
	id = db.Column(db.Integer, primary_key = True)
	image = db.Column(db.String(255), nullable= True)
	restaurant_id = db.Column(db.Integer, db.ForeignKey(Restaurants.id, ondelete='CASCADE'))
	title = db.Column(db.String(50))
	description = db.Column(db.Text)
	created_at_millis = db.Column(db.BIGINT, nullable=True)

	def __init__(restaurant_id, title, description, image):
		self.restaurant_id=restaurant_id
		self.title=title
		self.description=description
		self.image=image
		self.created_at_millis = int(time.time()*1000)

class Transactions(db.Model):
	__tablename__='transactions'
	id = db.Column(db.Integer, primary_key=True)
	restaurant_id = db.Column(db.Integer, db.ForeignKey(Restaurants.id, ondelete='CASCADE'))
	user_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'))
	subtotal = db.Column(db.Integer)
	adjustment_dollars = db.Column(db.Integer)
	adjustment_percent = db.Column(db.Integer)
	tax = db.Column(db.Integer)
	tip = db.Column(db.Integer)
	total = db.Column(db.Integer)
	created_at_millis = db.Column(db.BIGINT, nullable=True);

	def __init__(restaurant_id, user_id=None, subtotal=0, tax=13, adjustment_percent=0, adjustment_dollars=0, total=0, tip=0):
		self.created_at_millis = int(time.time()*1000)
		self.restaurant_id=restaurant_id
		self.user_id=user_id
		self.subtotal=subtotal
		self.tax=tax
		self.adjustment_dollars=0
		self.adjustment_percent=0
		self.total=total

class TransactionItems(db.Model):
	__tablename__='transaction_items'
	id = db.Column(db.Integer, primary_key=True)
	transaction_id = db.Column(db.Integer, db.ForeignKey(Transactions.id, ondelete='CASCADE'))
	item_id = db.Column(db.Integer, db.ForeignKey(MenuItems.id, ondelete='CASCADE'), nullable=True)
	subtotal = db.Column(db.Integer)
	adjustment_dollars = db.Column(db.Integer)
	adjustment_percent = db.Column(db.Integer)
	total = db.Column(db.Integer)

	def __init__(self, transaction_id, item_id, quantity=1, adjustment_dollars=0, adjustment_percent=0, subtotal=0, total=0):
		self.transaction_id=transaction_id
		self.item_id=item_id
		self.subtotal=subtotal
		self.adjustment_percent=adjustment_percent
		self.adjustment_dollars=self.adjustment_dollars
		self.total=total