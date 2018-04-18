from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:launchcodedb5@localhost:8889/Blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self,title,body,owner):
        self.title = title
        self.body = body
        self.owner = owner


    def is_valid(self):

        if self.title and self.body :
            return True
        else:
            return False

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref= 'owner')

    def __init__(self,username,password):
        self.username = username
        self.password = password


@app.route("/")
def index():
    
    return redirect("/blog")



 @app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        username = User.query.filter_by(username=username).first()
        if username and username.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')

            return render_template('login.html') 



@app.route('/signup', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            # TODO - user better response messaging
            return "<h1>Duplicate user</h1>"

return render_template('signup.html')  



@app.route("/blog")
def display_blog():
    entry_id = request.args.get('id')

    if (entry_id):
        entry = Blog.query.filter_by(id=entry_id).first()
        return render_template('main_blog.html',b_title="Build a Blog",entry=entry)
    else: 
        entry = ""   
        all_entries = Blog.query.all()
        return render_template('blog_id.html', b_title="Build a Blog",entry=entry,all_entries=all_entries)




@app.route('/newpost', methods=['GET','POST'])
def blog_page():
    title_error = ""
    body_error = ""
    new_title = ""
    new_body = ""
    owner = User.query.filter_by(username=session['username']).first()

    if request.method == "POST":
        new_title = request.form['title']
        new_body = request.form['body']
        add_blog = Blog(new_title,new_body,owner)

        if  new_title == ""  or len(new_body) == 1 :
             title_error = "Please Specify the blog title"
             title = ""
             # return render_template('new_post.html',title_error=title_error)

        if  new_body == "" or len(new_title) == 1 :
             body_error = "Please Specify the content of blog body"
             body = ""
            #return render_template('new_post.html',body_error=body_error)

             return render_template('new_post.html', title_error=title_error,body_error=body_error) 

        if not title_error and not body_error :
             db.session.add(add_blog)
             db.session.commit()
             url = "/blog?id=" + str(add_blog.id)
             return redirect(url)

    return render_template('new_post.html', b_title="Create a blog", title=new_title,body=new_body,
     title_error=title_error,body_error=body_error)



   
if __name__=="__main__":
  app.run()    