from flask import Flask, request, redirect, session, render_template, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:launchcodedb5@localhost:8889/Blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'wXT%Ywz4m+X#a9db'

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

   

@app.before_request
def require_login():
    allowed_routes = ['login','register','display_blog','index']
    if request.endpoint not in allowed_routes and 'username' not in session:
       return redirect('/login')        



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if not user :
            flash('user does not exist','error')
            return redirect('/signup')

        if username and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')
            return render_template('login.html') 

        if password == "" :
            flash('This password does not exists','error')
            return render_template('login.html')

        else:
            return redirect('signup.html')
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def register():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        v_pwd = request.form['v_pwd']

             
        if username == "" or password == "" or v_pwd == "" :
            flash('Username  or passwords cannot be empty.','error')
            username = ''
       
        else:
            if len(username) < 3 or len(username) > 20 or len(password) < 3 or len(password) > 20 or len(v_pwd) < 3 or len(v_pwd) > 20 :
                flash('Username  and passwords length 3-20 characters.','error')
                username = ''
      
        #if not len(password):
           # flash('Not a valid password','error')

       # if v_pwd == "" :
           # flash('Verify Password cannot be empty.','error')
             
        #elif len(v_pwd) <3 or len(v_pwd) > 20:
            #flash('Passwords do not match.','error')
    
        if password != v_pwd:
            flash('Passwords do not match','error')
            return redirect('/signup')

        existing_user = User.query.filter_by(username=username).first()

        if not existing_user:
            new_user = User(username,password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
           # flash('Username already exists')
            return redirect('/signup')

    return render_template('signup.html')  



@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')    


@app.route('/index', methods=['POST', 'GET'])
def index():

     usernames =  User.query.all()
     return render_template('index.html', usernames=usernames) 

    
    

@app.route("/blog")
def display_blog():
    entry_id = request.args.get('id')
    user_id = request.args.get('user')
    # username = User.query.filter_by(username=username).first()
    
    if user_id:
        blogs = Blog.query.filter_by(owner_id=user_id)
        return render_template('user_id.html', blogs=blogs)

    if entry_id:
        entry = Blog.query.filter_by(id=entry_id).first()
        return render_template('main_blog.html',entry=entry)

    else:
        entry = ""
        all_entries = Blog.query.all() 
        return render_template('blog_id.html',entry=entry,all_entries=all_entries)  


    # if user_id:
    #     blogs = Blog.query.filter_by(owner_id=user_id).first()
    #     return render_template('user_id.html',blogs=blogs) 
    # else: 
    #     blogs = Blog.query.all()
    #     return render_template('user_id.html',blogs=blogs)

    

    


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
        owner = User.query.filter_by(username=['username']).first()
        if  new_title == ""  or len(new_body) == 1 :
             flash("Please Specify the blog title",'error')
             title = ""
             # return render_template('new_post.html',title_error=title_error)

        if  new_body == "" or len(new_title) == 1 :
             flash("Please Specify the content of blog body",'error')
             body = ""
            #return render_template('new_post.html',body_error=body_error)

             return render_template('new_post.html') 

        if not title_error and not body_error :
             db.session.add(add_blog)
             db.session.commit()
             url = "/blog?id=" + str(add_blog.id)
             return redirect(url)

    return render_template('new_post.html', b_title="Create a blog", title=new_title,body=new_body)



   
if __name__=="__main__":
  app.run()    