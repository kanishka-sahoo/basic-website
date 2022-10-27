'''
Flask website
Author: Kanishka Sahoo
Date: 2022/10/27
'''

from flask import Flask, redirect, render_template, url_for

# initialise the server
app = Flask(__name__)

# Defining the home page of our site
@app.route("/")  # this sets the route to this page
def home():
	return render_template('index.html') # some basic inline html

if __name__ == "__main__":  # checks if program is run as a script or imported as module, and runs only if as script
    app.run()   # at 127.0.0.1:5000
