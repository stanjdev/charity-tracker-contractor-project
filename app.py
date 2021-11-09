from flask import Flask, render_template
import os
app = Flask(__name__)

@app.route('/')
def hello():
  return render_template('new-donation.html') 


@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/signup')
def signup():
  return render_template('signup.html')



@app.route('/new-donation')
def track_donation():
  return render_template('new-donation.html') 







if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

