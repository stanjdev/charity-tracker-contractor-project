from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

# MONGO_URI is Config Var for Heroku
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/charity_tracker')
client = MongoClient(host=host)

db = client.get_default_database()

# Donations resource in our MongoDB
donations = db.donations

# Charities resource in our MongoDB
charities = db.charities

app = Flask(__name__)



""" DONATIONS - RESTFUL ROUTES """

# GET - INDEX ROOT Route - HOME PAGE, ALL DONATIONS
@app.route('/')
def donations_index():
  return render_template('donations_index.html', donations=donations.find())

# GET - SHOW a specific donation from donation_id
@app.route('/donations/<donation_id>')
def donation_show_one(donation_id):
  donation = donations.find_one({'_id': ObjectId(donation_id)})
  return render_template('donation_show_one.html', donation=donation)

# GET - form to add NEW donation
@app.route('/donations/new')
def track_donation():
  donation = {}
  return render_template('donations_new.html', title='New Donation', donation=donation) 

# POST - CREATE / SUBMIT a donation
@app.route('/donations', methods=['POST'])
def donation_submit():
  donation = {
    'charity_name': request.form.get('charity_name'),
    'donation_amount': request.form.get('donation_amount'),
    'date_donated': request.form.get('date_donated'),
  }
  # WRITES TO THE donations DB
  donations.insert_one(donation)

  # Check if charity with same name exists. If not, insert one
  existing_charity = charities.find_one({'name': donation['charity_name']})
  if not existing_charity:
    charity = {
      'name': donation['charity_name'],
      'category': '',
      'about': '',
    }
    charities.insert_one(charity)

  return redirect(url_for('donations_index'))

# GET - EDIT form
@app.route('/donations/<donation_id>/edit')
def donation_edit_page(donation_id):
  donation = donations.find_one({'_id': ObjectId(donation_id)})
  return render_template('donations_edit.html', donation=donation, title='Edit Donation')

# PUT/PATCH - UPDATE a donation
@app.route('/donations/<donation_id>', methods=['POST'])
def donation_update(donation_id):
  # The newly updated form data
  updated_donation = {
    'charity_name': request.form.get('charity_name'),
    'donation_amount': request.form.get('donation_amount'),
    'date_donated': request.form.get('date_donated'),
  }
  # Set that former donation from db to this updated one
  donations.update_one(
    {'_id': ObjectId(donation_id)},
    {'$set': updated_donation}
  )
  return redirect(url_for('donations_index'))

# DELETE - a donation 
# USING AN <a> TAG WITHOUT POST METHOD WORKS
@app.route('/donations/<donation_id>/delete')
def donations_delete(donation_id):
  print(donation_id)
  donations.delete_one({'_id': ObjectId(donation_id)})
  return redirect(url_for('donations_index'))




# GET Profile page
@app.route('/profile')
def donor_profile():
  total_donated = 0
  for donation in donations.find():
    total_donated += int(donation['donation_amount'])
  print(total_donated)

  user = {
    'name': 'Stan',
    'total_donated': total_donated,
    'charities_donated_to': donations.find()
  }
  return render_template('profile.html', user=user, donations=donations.find(), charities=charities.find())






# GET ALL Charities /charities
@app.route('/charities')
def charities_all():
  return render_template('charities_all.html', charities=charities.find())


# GET SHOW one Charity profile page
# GET — /charities:/charity_name — SHOW one charity {k: v}
@app.route('/charities/<charity_name>')
def charity_profile(charity_name):
  charity = charities.find_one({'name': charity_name})

  return render_template('charity.html', charity=charity, donations=donations.find({'charity_name': charity_name}))

# # POST - /charities create a new charity when a new one is entered in the donation form
# ADDING A NEW DONATION CREATES ONE ALREADY.


# GET - EDIT form for charity
@app.route('/charities/<charity_name>/edit')
def charity_edit_form(charity_name):
  charity = charities.find_one({'name': charity_name})
  # get the charity object with the info to put in 'value' in each input
  return render_template('charity_edit_form.html', charity=charity)


# PUT/PATCH - UPDATE charity information
@app.route('/charities/<charity_name>', methods=['POST'])
def charities_update(charity_name):
  updated_charity = {
    'name': request.form.get('charity_name'),
    'category': request.form.get('charity_category'),
    'about': request.form.get('about_charity')
  }
  charities.update_one(
    {'name': charity_name},
    {'$set': updated_charity}
  )
  return redirect(url_for('charity_profile', charity_name=updated_charity['name']))







# GET login page
@app.route('/login')
def login_form():
  return render_template('login.html')

# POST to log user in
@app.route('/login', methods=['POST'])
def login():
  user = {
    'email': request.form.get('email'),
    'password': request.form.get('password')
  }
  print(user)
  return render_template('donations_new.html')

# GET sign up page
@app.route('/signup')
def signup_form():
  return render_template('signup.html')

# POST to register new user
@app.route('/signup', methods=['POST'])
def signup():
  new_user = {
    'email': request.form.get('email'),
    'password': request.form.get('password'),
    'confirm_password': request.form.get('confirm_password'),
  }
  print(new_user)
  return render_template('login.html')








if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

