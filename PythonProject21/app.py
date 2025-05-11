from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'PASSWORD'
app.config['MYSQL_DB'] = 'geeklogin'

mysql = MySQL(app)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/rome', methods=['GET', 'POST'])
def rome():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        if 'new_review' in request.form:
            if 'loggedin' in session:
                content = request.form['review_content']
                cursor.execute('INSERT INTO reviews (user_id, content) VALUES (%s, %s)', (session['id'], content))
                mysql.connection.commit()
            else:
                return redirect(url_for('login'))

        elif 'new_comment' in request.form:
            if 'loggedin' in session:
                review_id = request.form['review_id']
                content = request.form['comment_content']
                cursor.execute('INSERT INTO comments (review_id, user_id, content) VALUES (%s, %s, %s)',
                               (review_id, session['id'], content))
                mysql.connection.commit()
            else:
                return redirect(url_for('login'))

    # Fetch reviews and associated comments
    cursor.execute('''
        SELECT reviews.id AS review_id, reviews.content, accounts.username 
        FROM reviews JOIN accounts ON reviews.user_id = accounts.id
        ORDER BY reviews.id DESC
    ''')
    reviews_data = cursor.fetchall()

    # Fetch comments
    cursor.execute('''
        SELECT comments.review_id, comments.content, accounts.username 
        FROM comments JOIN accounts ON comments.user_id = accounts.id
        ORDER BY comments.id ASC
    ''')
    comments_data = cursor.fetchall()

    # Organize comments under each review
    reviews = []
    for review in reviews_data:
        review_comments = [c for c in comments_data if c['review_id'] == review['review_id']]
        reviews.append({
            'id': review['review_id'],
            'content': review['content'],
            'author': review['username'],
            'comments': review_comments
        })

    return render_template('rome.html', reviews=reviews)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return render_template('home.html', msg='Logged in successfully!')
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only letters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    return render_template('register.html', msg=msg)

@app.route('/about')
def about():
    # Logic for about page
    return render_template('about.html')

@app.route('/book')
def book():
    # Logic for about page
    return render_template('book.html')

@app.route('/cat')
def cat():
    # Logic for about page
    return render_template('cat.html')

@app.route('/contact')
def contact():
    # Logic for about page
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)