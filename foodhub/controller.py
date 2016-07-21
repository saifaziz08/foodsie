from foodhub import app
from models import *
from flask import render_template, request, flash, jsonify, abort, session
from forms import ContactForm
from flask.ext.mail import Message, Mail
import random

class Controller():
	__init__(self):
		pass

	@staticmethod
	def create_transaction(db_session, restaurant_id):
		transaction = Transactions(restaurant_id)
		db_session.add(transaction)
		db_session.flush()
		return transaction

	@staticmethod
	def update_transaction(db_session, transaction_id, subtotal=None, adjustment_dollars=None, adjustment_percent=None, tax=None, tip=None, code=None, card_hash=None, total=None):
		transaction = db_session.query(Transactions).filter_by(id=transaction_id).first()

		if subtotal is not None:
			transaction.subtotal = subtotal

		if adjustment_percent is not None:
			transaction.adjustment_percent = adjustment_percent

		if adjustment_dollars is not None:
			transaction.adjustment_dollars = adjustment_dollars

		if tax is not None:
			transaction.tax = tax

		if tip is not None:
			transaction.tax = tax

		user = None
		if code is not None:
			user = db_session.query(Users).filter_by(code=code).first()
		elif card_hash is not None:
			user = db_session.query(Users).filter_by(card_hash=card_hash).first()
			if user is None:
				user = Users(card_hash=card_hash)
				db_session.add(user)
				db_session.flush()
		points = -1
		if user:
			transaction.user_id = user.id
			points = user.points

		if total is not None:
			transaction.total = total

		db_session.add(transaction)
		db_session.flush()

		return points, transaction

	@staticmethod
	def finalize_transaction(db_session, user_id, transaction_id, points_used=None):
		user = db_session.query(Users).filter_by(id=user_id).first()
		if user.code:
			transaction = db_session.query(Transactions).filter_by(id=transaction_id).first()
			if points_used:
				user.points = 0
			else:
				user.points += int(transaction.total*0.1)
			db_session.add(user)
			
			transaction_meals = db_session.query(TransactionItems).filter_by(transaction_id=transaction_id).all()
			index = int(random.random()*len(transaction_meals))


			feedback = Feedback(transaction.restaurant_id, transaction_meals[index].item_id, user_id)
			db_session.add(feedback)
			db_session.flush()
		return user

	@staticmethod
	def delete_transaction(db_session, transaction_id):
		transaction = db_session.query(Transactions).filter_by(id=transaction_id).first()
		db_session.delete(transaction)
		db_session.flush()
		return

	@staticmethod
	def add_item_to_transaction(db_session, transaction_id, item_id):
		item = db_session.query(MenuItems).filter_by(id=item_id).first()
		transaction = db_session.query(Transactions).filter_by(id=transaction_id).first()
		trans_item = TransactionItems(transaction_id, item_id, subtotal=item.price, total=item.price)
		db_session.add(trans_item)
		db_session.flush()

	@staticmethod
	def update_item_in_transaction(db_session, transaction_id, item_id, quantity=None, adjustment_dollars=None,
								   adjustment_percent=None, subtotal=None, total=None):
		trans_item= db_session.query(TransactionItems).filter_by(item_id=item_id, transaction_id=transaction_id).first()
		if quantity:
			trans_item.quantity = quantity

		if adjustment_percent:
			trans_item.adjustment_percent = adjustment_percent

		if adjustment_dollars:
			trans_item.adjustment_dollars = adjustment_dollars

		if subtotal:
			trans_item.subtotal = subtotal

		if total:
			trans_item.total = total

		db_session.add(trans_item)
		db_session.flush()

		return trans_item

	@staticmethod
	def delete_transaction(db_session, transaction_id, item_id):
		trans_item= db_session.query(TransactionItems).filter_by(item_id=item_id, transaction_id=transaction_id).first()
		db_session.delete(trans_item)
		db_session.flush()
		return

	@staticmethod
	def update_feedback(db_session, feedback_id, stars, note):
		feedback = db_session.query(Feedback).filter_by(id=id).first()
		feedback.rating = stars
		feedback.note = note
		feedback.completed = 1
		db_session.add(feedback)
		db_session.flush()
		return

	@staticmethod
	def delete_feedback(db_session, feedback_id):
		feedback = db_session.query(Feedback).filter_by(id=id).first()
		db_session.delete(feedback)
		db_session.flush()
		return

	@staticmethod
	def add_menu_item(db_session, restaurant_id, name, desciption, category, price):
		item = MenuItems(restaurant_id, name, desciption, category, price)
		db_session.add(item)
		db_session.flush()
		return item

	@staticmethod
	def update_menu_item(db_session, item_id, name=None, desciption=None, category=None, price=None):
		item = db_session.query(MenuItems).filter_by(id=item_id).first()
		if name is not None:
			item.name = name

		if description is not None:
			item.description = description

		if category is not None:
			item.category = category

		if price is not None:
			item.price = price

		db_session.add(item)
		db_session.flush()

		return item

	@staticmethod
	def delete_menu_item(db_session, item_id):
		item = db_session.query(MenuItems).filter_by(id=item_id).first()
		db_session.delete(item)
		db_session.flush()
		return


