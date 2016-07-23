from foodhub import app
from models import *
from flask import render_template, request, flash, jsonify, abort, session
from forms import ContactForm
from flask.ext.mail import Message, Mail
 
mail = Mail()

@app.route('/testdb')
def testdb():
  if db.session.query('1').from_statement('SELECT 1').all():
    return 'GOT IT'
  else:
    return 'Jk'

@app.route('/signout')
def signout():
 
  if 'email' not in session:
    abort('400')
  session.pop('email', None)
  return jsonify({'result':'out'}, 200)

@app.route('/signup', methods=['POST'])
def signup():
  email = request.json.get('email', '')
  first_name = request.json.get('first_name', '')
  last_name = request.json.get('last_name', '')
  password = request.json.get('password', '')
  if not (email and first_name and last_name and password):
    abort(400)
  if db.session.query(User).filter_by(email=email).first():
    return abort(400)
  else:
    user = User(first_name, last_name, email, password)
    db.session.add(user)
    db.session.commit()
    session['email'] = user.email
    return jsonify({'result': 'success'}, 201)

@app.route('/signin', methods=['POST'])
def signin():
  email = request.json.get('email', '')
  password = request.json.get('password', '')
  user = db.session.query(User).filter_by(email=email).first()
  if not user:
    abort(400)
  if user.check_password(password):
    session['email'] = email
    return jsonify({'result': 'success'}, 200)
  else:
    abort(400)

@app.route('/')
@app.route('/Summary')
def home():
  return render_template('Summary.html')

@app.route('/Help')
def help():
  return render_template('Help.html')
  
@app.route('/MenuItems')
def menuItems():
	return render_template('menuItems.html')

@app.route('/Orders')
def orders():
	return render_template('orders.html')
	
@app.route('/PaymentMethods')
def paymentMethods():
	return render_template('paymentMethods.html')

@app.route('/Transactions')
def transactions():
	return render_template('transactions.html')
@app.route('/contact', methods=['GET', 'POST'])


def contact():
  form = ContactForm()

  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='contact@example.com', recipients=['your_email@example.com'])
      msg.body = """
      From: %s <%s>
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)

      return render_template('contact.html', success=True)

  elif request.method == 'GET':
    return render_template('contact.html', form=form)
