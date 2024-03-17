from flask import Flask,render_template,request,redirect
import models, db,utils
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from datetime import datetime
import traceback


app = Flask(__name__)

app.config["SECRET_KEY"] = "3jkshejkfhwleowjefkwe"

login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.user_loader # by default all user
def loader_user(user_id, db = db.db_session()):
    user = db.get(models.Users, user_id)
    db.close()
    return user


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/user/login/', methods = ["POST"])
def user_login(db = db.db_session()):
    try:
        login_data  = dict(request.form)
        user_name  = login_data["username"]
        password = login_data["password"]

        db_user  = select(models.Users).where(models.Users.Username == user_name)
        db_user = db.scalars(db_user).all()

        # if user does not exixst in database
        if db_user == []:
            db.close()
            return render_template("index.html", err_msg = f"{user_name} does not exists")
        
        # if user is existing
        db_user = db_user[0]
        hashed_pass = db_user.Pass

        verify_pass = utils.verify_pass(password, hashed_pass)
        if verify_pass == False:
            db.close()
            return render_template("index.html", err_msg = "Wrong password! Try Again")

        login_user(db_user)

        db.close()
        return redirect("/home/")
    
    except Exception as err:
        db.close()
        return {"detail": str(err)}


@app.route('/home/')
@login_required
def user_home(db = db.db_session()):
    db_category=select(models.Category)
    db_category=db.scalars(db_category).all()

    db_blogs = select(models.Blog).where(models.Blog.is_deleted == 0).options(joinedload(models.Blog.blog_user).load_only(
        models.Users.Firstname
        )).options(
            joinedload(models.Blog.blog_category).load_only(
                models.Category.category
                )).options(
            joinedload(models.Blog.blog_response).load_only(
                models.Response.response_type , models.Response.user_id,models.Response.response_args
                ))
    
    db_blogs = db_blogs.order_by(models.Blog.created_at.desc())

    db_blogs = db.scalars(db_blogs).unique().all()
    db.close()
    return render_template("home.html", categories=db_category, blog_data = db_blogs)


@app.route('/user/logout/')
@login_required
def user_logout():
    logout_user()
    return redirect("/")
        
        



@app.route('/user/signup/',methods=["POST"])
def user_signup(db = db.db_session()):
    try:
        form_data = dict(request.form)

        db_user = select(models.Users).where(models.Users.email == form_data["email"])
        db_user = db.scalars(db_user).all()
        # print("Check user with email -> ", db_user)

        # # Check if the user with the given email already exists
        if db_user != []:
            db.close()
            return render_template("index.html", err_msg = f"User with {form_data['email']} already exists")
        
        new_user = models.Users()

        new_user.Firstname = form_data["f_name"]
        new_user.Lastname = form_data["l_name"]
        new_user.email = form_data["email"]
        new_user.contact = form_data["contact"]
        new_user.Pass = utils.get_hased_pass(form_data["password"])
        new_user.Created_at = datetime.now()
        new_user.Updated_at = datetime.now()
        new_user.Username = form_data["email"]

        db.add(new_user)
        db.commit()

        db.close()
        mail_body = f"""
                    Hi {form_data["f_name"]},

                    Your new account has been created with us, please log in using your email or username.
                    Hope you like our services

                    
                    Team BlogU
                    """
        utils.send_mail(to = form_data["email"], subject="Hello from BlogU 👋", mail_body=mail_body)
        return redirect("/")

        
    
    except Exception as err:
        # Rollback changes in case of an error
        db.close()
        return {"detail": str(err)}

#for edit profile
@app.route('/user/update/', methods=["POST"])
@login_required
def user_update(db = db.db_session()):
    try:
        form_data = dict(request.form)
        print("Check user with email -> ", form_data)

        db_user = select(models.Users).where(models.Users.email == form_data["email"])
        db_user = db.scalars(db_user).all()
        

        db_user = db_user[0]
        

        db_user.Firstname = form_data["f_name"]
        db_user.Lastname = form_data["l_name"]
        db_user.contact = form_data["contact"]
        #new_user.username = form_data["email"]
        # new_user.password = utils.get_hased_pass(form_data["password"])
        # new_user.created_at = datetime.now()
        db_user.Updated_at = datetime.now()

        db.commit()

        db.close()
        return redirect("/home/")
        
    except Exception as err:
        
        db.close()
        return {"detail": str(err)}

#for change password
@app.route('/user/changepassword/', methods = ["POST"])
@login_required
def user_change_password(db = db.db_session()):
    try:
        form_data = dict(request.form)
        
        old_pass = form_data["old_password"]
        new_pass = form_data["new_password"]

        user_id = current_user.id
        db_user = db.get(models.Users, user_id)
        
        if not utils.verify_pass(old_pass, db_user.Pass) :
            db.close()
            return render_template("home.html", args = True)
        
        new_hashed_pass = utils.get_hased_pass(new_pass)
        db_user.Pass = new_hashed_pass

        db.commit()
        db.close()
        return redirect("/home/")

    except Exception as err:
        db.close()
        return {"detail":str(err)}, 401

#for forgot password
@app.route('/user/forgotpassword/')
def forgot_password(db = db.db_session()):
    try:
        email = request.args.get("email")
        db_user = select(models.Users).where(models.Users.email == email)
        db_user = db.scalars(db_user).all()
        
        # checking the user with email
        if db_user == []:
            db.close()
            return render_template("index.html", err_msg = f"User with {email} does not exists")
        
        db_user = db_user[0]
        hashed_pass = utils.reset_password(db_user.email, db_user.Firstname)
        db_user.Pass = hashed_pass
        db.commit()
        db.close()
        return  render_template("index.html", err_msg = f"New password has been sent on your email")
    except Exception as err:
        db.close()
        return {"detail":str(err)}


@app.route('/blog/create/', methods= ['POST'])
@login_required
def create_blog(db = db.db_session()):
    try:
        form_data=dict(request.form)
        new_blog=models.Blog()

        new_blog.user_id = current_user.id
        new_blog.content=form_data["blog_content"]
        new_blog.title = form_data["blog_title"]
        new_blog.category_id=form_data["category"]
        new_blog.is_deleted= 0
        new_blog.created_at= datetime.now()
        new_blog.updated_at= datetime.now()
        
        db.add(new_blog)
        db.commit()

        db.close()

        return redirect('/home/')

    except Exception as err:
        db.close()
        return {"detail": str(err)}, 403


@app.route('/blogs/like/')
@login_required
def like_blog(db = db.db_session()):
    try:
        blog_id= request.args.get("blog_id")

        db_blog = select(models.Blog).where((models.Blog.id == blog_id),(models.Blog.is_deleted == 0))
        db_blog = db.scalars(db_blog).all()

        if not db_blog:
            db.close()
            return{"detail": "invalid blog_id"},400

        db_response = select(models.Response).where((models.Response.blog_id == blog_id),
                                                    (models.Response.response_type == 1),
                                                    (models.Response.user_id == current_user.id)
                                                    )
        db_response = db.scalars(db_response).first()
        
        if db_response:
            db.delete(db_response)
            db.commit()
            db.close()

            return redirect('/home/')
        
        new_resp= models.Response()
        new_resp.blog_id = blog_id
        new_resp.user_id = current_user.id
        new_resp.response_type = 1
        
        
        db.add(new_resp)
        db.commit()
        db.close()

        return redirect('/home/')



    except Exception as err:
        db.close()
        return {"detail":str(err)},403


@app.route('/home/myblogs/')
@login_required
def my_blogs(db = db.db_session()):
    try:
        db_category = select(models.Category)
    
        db_category = db.scalars(db_category).all()

        db_blogs = select(models.Blog).where((models.Blog.user_id == current_user.id),(models.Blog.is_deleted == 0)).options(joinedload(models.Blog.blog_user).load_only(
            models.Users.Firstname
            )).options(
                joinedload(models.Blog.blog_category).load_only(
                    models.Category.category, models.Category.id
                    )).options(
                joinedload(models.Blog.blog_response).load_only(
                    models.Response.response_type, models.Response.user_id, models.Response.response_args
                    ))
        db_blogs = db_blogs.order_by(models.Blog.updated_at.desc())
        
        db_blogs = db.scalars(db_blogs).unique().all()
        db.close()
        
        return render_template("blogs.html", categories = db_category, blog_data = db_blogs)
    except Exception as err:
        db.close()
        return {"details":str(err)}, 403

@app.route('/blogs/update/', methods = ["POST"])
@login_required
def update_post(db = db.db_session()):
    try:
        form_data = dict(request.form)
        blog_id = int(request.args.get("blog_id"))

        db_blog = db.get(models.Blog, blog_id)
        db_blog.title = form_data['blog_title']
        db_blog.content = form_data['blog_content']
        db_blog.category_id = form_data['category']
        db_blog.updated_at = datetime.now()
        
        db.commit()
        db.close()

        return redirect('/home/myblogs/')

    except Exception as err:
        db.close()
        traceback.print_exc()
        return {"details":str(err)}, 403

@app.route('/blogs/delete/')
@login_required
def delete_post(db = db.db_session()):
    try:
        
        blog_id = int(request.args.get("blog_id"))

        db_blog = db.get(models.Blog, blog_id)
        
        db_blog.is_deleted = 1
        
        db.commit()
        db.close()

        return redirect('/home/myblogs/')

    except Exception as err:
        db.close()
        traceback.print_exc()
        return {"details":str(err)}, 403



if __name__=="__main__":
    app.run(debug=True)



