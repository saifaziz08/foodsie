from flask.ext.wtf import Form
from wtforms.fields import TextField, TextAreaField, SubmitField
from wtforms.validators import Required, Email

class ContactForm(Form):
  name = TextField("Name",  [Required("Please enter your name.")])
  email = TextField("Email",  [Required("Please enter your email address."), Email("Please enter your email address.")])
  subject = TextField("Subject",  [Required("Please enter a subject.")])
  message = TextAreaField("Message",  [Required("Please enter a message.")])
  submit = SubmitField("Send")
