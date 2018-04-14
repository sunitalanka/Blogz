from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:launchcodedb2@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self,title,body):
        self.title = title
        self.body = body
 
def display_bolgs():
    blog_id = Blog.query.all()

@app.route('/blog', methods=['POST', 'GET'])
def blog_page():

    if request.method == "POST":
        blog = request.form['blog']
        new_blog_title = request.form['blog_title']
        new_blog_body = request.form['blog_body'] 

        if (not new_blog_title) or (new_blog_title == ""):
            title_error = "Please Specify the blog title"
            return render_template('new_post.html',title_error=title_error)
    
        if (not new_blog_body) or (new_blog_body == ""):
            body_error = "Plese add some content to blog body"
            return render_template('new_post.html',body_error=body_error)
        
        else:
             add_blog = Blog(new_blog_title,new_blog_body) 
             db.session.add(add_blog)
             db.session.commit()
             return render_template('main_blog.html',blogs=display_bolgs())

    return render_template('main_blog.html', blogs=display_bolgs())

@app.route('/newpost', methods=['POST','GET'])
def add_blog():
      return render_template('new_post.html')


@app.route('/blog?id=id', methods=['POST','GET']) 
def blog_id():
    blog_title = request.form('blog_title')
    blog_body = request.form('blog_body') 
    return render_template('blog_id.html', blog_title=blog_title,blog_body=blog_body) 

   
    

if __name__ == '__main__':
   app.run()    