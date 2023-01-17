'''
Flask website
Author: Kanishka Sahoo
Date: 2022/10/27
'''
import sqlite3
from flask import Flask, flash, redirect, render_template, url_for, flash, request
from werkzeug.exceptions import abort
import logging

# Get Database Connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

# initialise the server
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.before_request
def log_request():
    # ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    logging.basicConfig(filename='requests.log', level=logging.DEBUG)
    logging.debug(f'{request.method} {request.url}')

# Defining the home page of our site
@app.route("/")  # this sets the route to this page
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts) # some basic inline html

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')
'''
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)
'''
if __name__ == "__main__":  # checks if program is run as a script or imported as module, and runs only if as script
	app.run(host='0.0.0.0')
