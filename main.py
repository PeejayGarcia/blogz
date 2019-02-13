from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model): 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title = title   
        self.body = body


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blogs = Blog.query.all()

    return render_template('blog.html', title="Build-A-Blog", blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])  
def newpost():
    blogs = Blog.query.all()
    
    if request.method == 'POST':
        blog_title = request.form['title']
        body = request.form['body']
        new_blog = Blog(blog_title, body)
        db.session.add(new_blog)
        db.session.commit()

        encoded_error = request.args.get("error")

        return render_template('blog.html', title="Build-A-Blog", blogs=blogs, blog_title=blog_title, 
            body=body, error=encoded_error and cgi.escape(encoded_error, quote=True))
    
    return render_template('newpost.html', blogs=blogs)


@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/blog')


if __name__ == '__main__':
    app.run()