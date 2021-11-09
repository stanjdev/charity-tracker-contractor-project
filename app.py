from flask import Flask, render_template, request
import os
# from bson.objectid import ObjectId



app = Flask(__name__)


# ROOT Route
@app.route('/')
def charity_tracker_index():
  return render_template('new_donation.html') 


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
  return render_template('new_donation.html')

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

# GET the form to track donation
@app.route('/donation/new')
def track_donation():
  return render_template('new_donation.html') 

# POST - SUBMIT a donation
@app.route('/donation', methods=['POST'])
def donation_submit():
  donation = {
    'charity_name': request.form.get('charity_name'),
    'amount_in_cents': request.form.get('donation_amount'),
    'date': request.form.get('date_donated'),
  }
  print(donation)
  # insert_one(donation) to the donations database
  return render_template('new_donation.html')


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

