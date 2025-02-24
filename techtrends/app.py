import sqlite3
import logging
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import sys

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

db_connection_counter = 0

# Set up logging to output to STDERR
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    datefmt='%d/%m/%Y %H:%M:%S',
                    stream=sys.stderr)

# Create a logger for the application
app_logger = logging.getLogger('app')

# Function to get a database connection.
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    print(f'Querying for post with ID: {post_id}')
    app_logger.debug(f'Querying for post with ID: {post_id}')
    post = connection.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    if post is None:
        app_logger.warning(f'No post found with ID: {post_id}')
    connection.close()
    return post

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    global db_connection_counter  # Declare that we are using the global variable
    db_connection_counter += 1  # Increment the connection count
    connection.close()
    print('Index page accessed.')
    app_logger.info('Index page accessed.')
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app_logger.warning(f'Article with ID {post_id} not found. Returning 404.')
        return render_template('404.html'), 404
    else:
        print(f'Article "{post["title"]}" retrieved.')
        app_logger.info(f'Article "{post["title"]}" retrieved.')
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    print('About Us page accessed.')
    app_logger.info('About Us page accessed.')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            print(f'New article "{title}" created.')
            app_logger.info(f'New article "{title}" created.')
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/healthz', methods=['GET'])
def health_check():
    return jsonify({"result": "OK - healthy"}), 200

db_connection_count = 0  # Initialize a global variable to count database connections

def get_post_count():
    connection = get_db_connection()
    count = connection.execute('SELECT COUNT(*) FROM posts').fetchone()[0]
    connection.close()
    return count

@app.route('/metrics', methods=['GET'])
def metrics():
    post_count = get_post_count()  # Get the total number of posts
    db_connection_count = db_connection_counter  # Replace with your actual counter variable

    return jsonify({
        "post_count": post_count,
        "db_connection_count": db_connection_count
    }), 200

# Start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111')
