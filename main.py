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
 


    def is_valid(self):

        if self.title and self.body :
            return True
        else:
            return False



@app.route("/")
def index():
    
    return redirect("/blog")



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

    if request.method == "POST":
        new_title = request.form['title']
        new_body = request.form['body']
        add_blog = Blog(new_title,new_body)

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