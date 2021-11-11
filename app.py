from flask import Flask, render_template, request, redirect, url_for
import os
from pymongo import MongoClient
from bson.objectid import ObjectId

# MONGO_URI is Config Var for heroku later.
host = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/charity_tracker')
client = MongoClient(host=host)
db = client.get_default_database()

# Donations resource in our MongoDB
donations = db.donations


app = Flask(__name__)




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
  # WRITES TO THE DB
  donations.insert_one(donation)
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
  return render_template('profile.html')

# GET Charity profile page
@app.route('/charity')
def charity_profile():
  return render_template('charity.html')




if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

