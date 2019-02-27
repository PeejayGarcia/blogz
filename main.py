from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'Ampongan'

class Blog(db.Model): 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title   
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before.reque



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in.")
            print(session)
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')



@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            return "<h1>Duplicate user</h1>"
        
    return render_template('register.html')



@app.route('/blog', methods=['POST', 'GET'])
def blog():
    view = 'default'
    blogs = []

    if request.args:
        id = request.args.get('id')
        username = request.args.get('user')
        if id:
            blogs.append(Blog.query.get(id))
            view = 'single'
        else:
            owner = User.query.filter_by(username = username).first()
            blogs = Blog.query.filter_by(owner = owner).all()
    else:
        blogs = Blog.query.all()    


    return render_template('blog.html', title="Blogz", blogs=blogs, view=view)


@app.route('/newpost', methods=['POST', 'GET'])  
def newpost():
    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        blog_title = request.form['title']
        body = request.form['body']
        new_blog = Blog(blog_title, body)
        db.session.add(new_blog)
        db.session.commit()

        encoded_error = request.args.get("error")

        return render_template('newpost.html', title="Blogz", blogs=blogs, blog_title=blog_title, 
            body=body, error=encoded_error and cgi.escape(encoded_error, quote=True))
    
    return render_template('newpost.html', blogs=blogs)


@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/blog')


if __name__ == '__main__':
    app.run()