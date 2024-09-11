import datetime
import os
from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request, jsonify
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import (RegisterForm, LoginForm,PostForm,Bid,close)
from fpdf import FPDF
 # ,CreatePostForm, , CommentForm)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email = "agreedeal1@gmail.com"
password = "zcvt pwvg bhgx qflt"
subject = "Successful Bid Confirmation"




app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class User(UserMixin,db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(250), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    role: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)

# class FarmerPost(db.Model):
#     __tablename__ = "farmer_posts"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     # farmer_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
#     # farmer = relationship("User", back_populates="posts")
#     title: Mapped[str] = mapped_column(String(250), nullable=False)
#     location: Mapped[str] = mapped_column(String(250), nullable=False)
#     date: Mapped[str] = mapped_column(String(250), nullable=False)
#     harvest: Mapped[str] = mapped_column(String(250), nullable=False)
#     amount: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
#     baseprice: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
#     highest: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
#     img_url: Mapped[str] = mapped_column(String(250), nullable=False)
#     body: Mapped[str] = mapped_column(Text, nullable=False)
#     # Parent relationship to the comments
#     # comments = relationship("Comment", back_populates="parent_post")

# class Posts(db.Model):
#     __tablename__ = "posts"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     # farmer_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
#     # farmer = relationship("User", back_populates="posts")
#     title: Mapped[str] = mapped_column(String(250), nullable=False)
#     location: Mapped[str] = mapped_column(String(250), nullable=False)
#     date: Mapped[str] = mapped_column(String(250), nullable=False)
#     harvest: Mapped[str] = mapped_column(String(250), nullable=False)
#     amount: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
#     baseprice: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
#     highest: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
#     img_url: Mapped[str] = mapped_column(String(250), nullable=False)
#     body: Mapped[str] = mapped_column(Text, nullable=True)
#     # Parent relationship to the comments
#     # comments = relationship("Comment", back_populates="parent_post")

# class CropPosts(db.Model):
#     __tablename__ = "crop_posts"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     farmer_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
#     farmer = relationship("User", back_populates="posts")
#     title: Mapped[str] = mapped_column(String(250), nullable=False)
#     location: Mapped[str] = mapped_column(String(250), nullable=False)
#     date: Mapped[str] = mapped_column(String(250), nullable=False)
#     harvest: Mapped[str] = mapped_column(String(250), nullable=False)
#     amount: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
#     baseprice: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
#     highest: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
#     img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    # body: Mapped[str] = mapped_column(Text, nullable=True)
    # Parent relationship to the comments
    # comments = relationship("Comment", back_populates="parent_post")

# class Farmer_Posts(db.Model):
#     __tablename__ = "f_posts"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     title: Mapped[str] = mapped_column(String(250), nullable=False)
#     location: Mapped[str] = mapped_column(String(250), nullable=False)
#     date: Mapped[str] = mapped_column(String(250), nullable=False)
#     harvest: Mapped[str] = mapped_column(String(250), nullable=False)
#     amount: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
#     baseprice: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
#     highest: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
#     highest_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
#     img_url: Mapped[str] = mapped_column(String(250), nullable=False)

# class Farmer_Post(db.Model):
#     __tablename__ = "farmer_post"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     title: Mapped[str] = mapped_column(String(250), nullable=False)
#     farmer_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
#     location: Mapped[str] = mapped_column(String(250), nullable=False)
#     date: Mapped[str] = mapped_column(String(250), nullable=False)
#     harvest: Mapped[str] = mapped_column(String(250), nullable=False)
#     amount: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
#     baseprice: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
#     highest: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
#     highest_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
#     img_url: Mapped[str] = mapped_column(String(250), nullable=True)

class F_post(db.Model):
    __tablename__ = "f_post"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    farmer_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    harvest: Mapped[str] = mapped_column(String(250), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    baseprice: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    highest: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    highest_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=True)
    end: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)

# class Contract(db.Model):
#     __tablename__ = "contract"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     contract_date: Mapped[str] = mapped_column(String(250), nullable=False)
#     total_amount: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
#     transportation_amount: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
#     goods_amount: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
#     goods_name: Mapped[str] = mapped_column(String(250), nullable=False)
#     goods_quantity: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
#     farmer_name: Mapped[str] = mapped_column(String(250), nullable=False)
#     buyer_name: Mapped[str] = mapped_column(String(250), nullable=False)
#     deliver_address: Mapped[str] = mapped_column(String(250), nullable=False)
#     delivery_date: Mapped[str] = mapped_column(String(250), nullable=False)
#
# class Contracts(db.Model):
#     __tablename__ = "contracts"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     contract_date: Mapped[str] = mapped_column(String(250), nullable=False)
#     total_amount: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
#     transportation_amount: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
#     goods_amount: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
#     goods_name: Mapped[str] = mapped_column(String(250), nullable=False)
#     goods_quantity: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
#     farmer_name: Mapped[str] = mapped_column(String(250), nullable=False)
#     buyer_name: Mapped[str] = mapped_column(String(250), nullable=False)
#     deliver_address: Mapped[str] = mapped_column(String(250), nullable=False)
#     delivery_date: Mapped[str] = mapped_column(String(250), nullable=False)
#     post_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)

class User_Contracts(db.Model):
    __tablename__ = "user_contracts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    contract_date: Mapped[str] = mapped_column(String(250), nullable=False)
    total_amount: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    transportation_amount: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    goods_amount: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    goods_name: Mapped[str] = mapped_column(String(250), nullable=False)
    goods_quantity: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    farmer_name: Mapped[str] = mapped_column(String(250), nullable=False)
    buyer_name: Mapped[str] = mapped_column(String(250), nullable=False)
    deliver_address: Mapped[str] = mapped_column(String(250), nullable=False)
    delivery_date: Mapped[str] = mapped_column(String(250), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    status: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)

# class Confirmed_Contracts(db.Model):
#     __tablename__ = "confirmed_contracts"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     farmer_username: Mapped[str] = mapped_column(String(250), unique=False, nullable=True)
#     farmer_phonenumber: Mapped[str] = mapped_column(String(250), unique=False, nullable=True)
#     consumer_username: Mapped[str] = mapped_column(String(250), unique=False, nullable=True)
#     consumer_phonenumber: Mapped[str] = mapped_column(String(250), unique=False, nullable=True)
#     transaction_id: Mapped[str] = mapped_column(String(250), unique=False, nullable=True)
#     total_amount: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
#     payment_status: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
#     delivery_status: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
#     settlement_to: Mapped[str] = mapped_column(String(250), unique=False, nullable=True)

class Confirmed_Contract(db.Model):
    __tablename__ = "confirmed_contract"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=False, nullable=True)
    farmer_username: Mapped[str] = mapped_column(String(250), unique=False, nullable=True)
    farmer_phonenumber: Mapped[str] = mapped_column(String(250), unique=False, nullable=True)
    consumer_username: Mapped[str] = mapped_column(String(250), unique=False, nullable=True)
    consumer_phonenumber: Mapped[str] = mapped_column(String(250), unique=False, nullable=True)
    transaction_id: Mapped[str] = mapped_column(String(250), unique=False, nullable=True)
    total_amount: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    payment_status: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    delivery_status: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    settlement_to: Mapped[str] = mapped_column(String(250), unique=False, nullable=True)

class Chats(db.Model):
    __tablename__ = "chats"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    farmer_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    posted_by: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)
    msg: Mapped[str] = mapped_column(String(250), unique=False, nullable=True)
with app.app_context():
    db.create_all()


def find_user(id):
    result = db.session.execute(db.select(User).where(User.id == id))
    user = result.scalar()
    print(user)
    return user

def find_contract(id):
    result = db.session.execute(db.select(User_Contracts).where(User_Contracts.post_id == id))
    user = result.scalar()
    print(user)
    return user

# Bootstrap5(app)
#
# class Base(DeclarativeBase):
#     pass
#
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
# db = SQLAlchemy(model_class=Base)
# db.init_app(app)




# class Consumer(db.Model):
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     username: Mapped[str] = mapped_column(String(250), unique=False, nullable=False)
#     email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
#     password: Mapped[str] = mapped_column(String(250), nullable=False)

# with app.app_context():
#     db.create_all()
# with app.app_context():
#     new_book = User(id=1, username="adminfarmer", email="adminfarmer@gmail.com", password="123",role=0)
#     db.session.add(new_book)
#     db.session.commit()
class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", size=12)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", size=8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

@app.route("/")
def home():
    return render_template("index.html")



@app.route('/login/farmer', methods=["GET", "POST"])
def farmer_login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('farmer_login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('farmer_login'))
        else:
            login_user(user)
            return redirect(url_for('farmer_home'))

    return render_template("login.html", form=form)

@app.route('/login/user', methods=["GET", "POST"])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('user_login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('user_login'))
        else:
            login_user(user)
            return redirect(url_for('user_home'))

    return render_template("userlogin.html", form=form)

@app.route("/signup/farmer", methods=["GET", "POST"])
def farmer_sign_up():
    form=RegisterForm()
    if form.validate_on_submit():
        # Check if user email is already present in the database.
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('farmer_login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            username=form.name.data,
            password=hash_and_salted_password,
            role=0
        )
        db.session.add(new_user)
        db.session.commit()
        print(form.email.data)
        login_user(new_user)
        return redirect(url_for("farmer_home"))
    return render_template("signup.html",form=form)

@app.route("/signup/user", methods=["GET", "POST"])
def user_sign_up():
    form=RegisterForm()
    if form.validate_on_submit():
        # Check if user email is already present in the database.
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('user_login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            username=form.name.data,
            password=hash_and_salted_password,
            role=1
        )
        db.session.add(new_user)
        db.session.commit()
        print(form.email.data)
        login_user(new_user)
        return redirect(url_for("user_home"))
    return render_template("usersignup.html",form=form)

@app.route("/user/home")
def user_home():
    result = db.session.execute(db.select(F_post))
    posts = result.scalars().all()
    return render_template("userhome.html",all_posts=posts, current_user=current_user)

@app.route("/farmer/home", methods=["GET", "POST"])
def farmer_home():

    result = db.session.execute(db.select(F_post).where(F_post.farmer_id == current_user.id))
    posts = result.scalars().all()
    for post in posts:
        print(post.title)
    print(posts)
    form = PostForm()
    if form.validate_on_submit():
        if form.img_url.data=="":
            new_post = F_post(
                title=form.title.data,
                farmer_id=current_user.id,
                location=form.location.data,
                date=form.date.data,
                harvest=form.harvest.data,
                amount=form.amount.data,
                baseprice=form.baseprice.data,
                highest=form.baseprice.data,
                end=0,
                img_url="https://images.unsplash.com/photo-1590779033100-9f60a05a013d?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
            )
        else:
            new_post = F_post(
            title=form.title.data,
            farmer_id=current_user.id,
            location=form.location.data,
            date=form.date.data,
            harvest=form.harvest.data,
            amount=form.amount.data,
            baseprice=form.baseprice.data,
            highest=form.baseprice.data,
            img_url=form.img_url.data,
            end=0
        )
        db.session.add(new_post)
        db.session.commit()
        flash("Sucessfully Posted.")
        return redirect(url_for("farmer_home"))
    return render_template("farmerhome.html", form=form,posts=posts, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/user/post/<int:f_post_id>", methods=["GET", "POST"])
def show_post(f_post_id):
    form = Bid()
    requested_post = db.get_or_404(F_post,f_post_id)
    farmer= find_user(requested_post.farmer_id)
    user = find_user(requested_post.highest_id)
    if form.validate_on_submit():
        if (str(form.bid.data)>str(requested_post.highest)):
            requested_post.highest=form.bid.data
            requested_post.highest_id=current_user.id
            db.session.commit()
            farmer = find_user(requested_post.farmer_id)
            user = find_user(requested_post.highest_id)
        return render_template("user_post.html",form=form, post=requested_post, current_user=current_user,farmer=farmer, high=user)

    return render_template("user_post.html",form=form, post=requested_post, current_user=current_user,farmer=farmer, high=user)

@app.route("/farmer/post/<int:f_post_id>", methods=["GET", "POST"])
def show_post_farmer(f_post_id):
    form=close()

    requested_post = db.get_or_404(F_post,f_post_id)
    farmer = find_user(requested_post.farmer_id)
    user = find_user(requested_post.highest_id)
    if form.validate_on_submit():
        requested_post.end=1
        db.session.commit()
        message = MIMEMultipart()
        message["From"] = email
        message["To"] = user.email
        message["Subject"] = subject

        body = (f"Dear {user.username},\n"
                "We are pleased to inform you that your bid has been successful! You have won the auction for the following \n"
                f"Item Product:{requested_post.title} \n"
                f"Bid Amount: ₹{requested_post.highest} \n"
                "Congratulations on securing this purchase. To proceed with the next steps, please visit your order’s page.\n"
                "Thank you for participating, and we look forward to serving you.\n"
                "Best regards,\nAgreeDeal")

        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(from_addr=email, to_addrs=user.email, msg=message.as_string())
        return render_template("farmer_post.html",form=form, post=requested_post, current_user=current_user,farmer=farmer, high=user)
    return render_template("farmer_post.html",form=form, post=requested_post, current_user=current_user,farmer=farmer, high=user)

@app.route("/delete/<int:f_post_id>")
def delete_post(f_post_id):
    post_to_delete = db.get_or_404(F_post, f_post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('farmer_home'))

@app.route("/farmer/orders")
def farmer_orders():
    result = db.session.execute(db.select(F_post))
    posts = result.scalars().all()
    return render_template("farmer_orders.html",all_posts=posts, current_user=current_user)

@app.route("/user/orders")
def user_orders():
    result = db.session.execute(db.select(F_post))
    posts = result.scalars().all()
    return render_template("user_orders.html",all_posts=posts, current_user=current_user)

@app.route('/user/<int:u_id>/<int:post_id>', methods=["GET", "POST"])
def buyer_form(u_id,post_id):
    return render_template('buyer_form.html',current_user=current_user,user_id=u_id,post_id=post_id)

@app.route('/submited/contract/<int:post_id>', methods=["GET", "POST"])
def sub_contract(post_id):

    new_contract = User_Contracts(
        contract_date=request.form.get('date'),
        total_amount=request.form.get('total_amount'),
        transportation_amount=request.form.get('transportation_amount'),
        goods_amount=request.form.get('goods_amount'),
        farmer_name=request.form.get('farmer_name'),
        buyer_name=request.form.get('buyer_name'),
        goods_quantity=request.form.get('goods_quantity'),
        goods_name=request.form.get('goods_name'),
        deliver_address=request.form.get('delivery_address'),
        delivery_date=request.form.get('delivery_date'),
        post_id=post_id,
        status=0
    )
    db.session.add(new_contract)
    db.session.commit()
    result = db.session.execute(db.select(F_post).where(F_post.id == post_id))
    result = result.scalar()
    result.end=-1
    db.session.commit()
    return render_template("contract_success.html", current_user=current_user)

@app.route('/farmer/orders/confirm/<int:post_id>', methods=["GET", "POST"])
def approve(post_id):
    result = db.session.execute(db.select(User_Contracts).where(User_Contracts.post_id == post_id))
    result=result.scalar()

    return render_template("farmer_form.html",contract=result)

@app.route('/orders/confirm/download/<int:contract_id>', methods=["GET", "POST"])
def contract_confirmation(contract_id):
    response = request.form.get('response')
    if response == 'confirm':
        result = db.session.execute(db.select(User_Contracts).where(User_Contracts.id == contract_id))
        result = result.scalar()
        result.status=1
        db.session.commit()
        result1 = db.session.execute(db.select(F_post).where(F_post.id == result.post_id))
        result1 = result1.scalar()
        result1.end = 10
        db.session.commit()

        new_admin_contract = Confirmed_Contract(
            title=result.goods_name,
            farmer_username=result.farmer_name,
            farmer_phonenumber=123,
            consumer_username=result.buyer_name,
            consumer_phonenumber=321,
            total_amount=result.total_amount,
            payment_status=0,
            delivery_status=0,
        )
        db.session.add(new_admin_contract)
        db.session.commit()

        return render_template('confirmation.html')
    elif response == 'reject':
        result = db.session.execute(db.select(User_Contracts).where(User_Contracts.id == contract_id))
        result = result.scalar()
        result.status = -1
        db.session.commit()
        result1 = db.session.execute(db.select(F_post).where(F_post.id == result.post_id))
        result1 = result1.scalar()
        result1.end = 10
        db.session.commit()
        return render_template('rejection.html')
    else:
        return redirect(url_for('farmer_form'))

@app.route('/farmer/orders/<int:post_id>', methods=["GET", "POST"])
def contract_display(post_id):
    contract=find_contract(post_id)
    result = db.session.execute(db.select(User_Contracts).where(User_Contracts.id == contract.id))
    result = result.scalar()
    if result.status==1:
        generate_contract(result)
        return render_template('confirmation.html')
    elif result.status == -1:
        return render_template('rejection.html')
    else:
        return render_template('waiting_farmer.html')

@app.route('/user/orders/<int:post_id>', methods=["GET", "POST"])
def user_contract_display(post_id):
    contract=find_contract(post_id)
    result = db.session.execute(db.select(User_Contracts).where(User_Contracts.id == contract.id))
    result = result.scalar()
    if result.status==1:
        generate_contract(result)
        return render_template('user_confirmation.html',post_id=post_id)
    elif result.status == -1:
        return render_template('rejection.html')
    else:
        return render_template('waiting_farmer.html')

@app.route('/payment/<int:post_id>', methods=["GET", "POST"])
def payment(post_id):
        return render_template('payment.html')


@app.route('/negotiate/<int:farmer_id>/<int:user_id>', methods=["GET", "POST"])
def negotiate(farmer_id ,user_id):
    if request.method == "POST":
        message = request.form["message"]
        new_msg = Chats(
            farmer_id=farmer_id+1000,
            user_id=user_id+10000,
            posted_by=current_user.id,
            msg=message
        )
        db.session.add(new_msg)
        db.session.commit()
        return redirect(url_for('refresh', farmer_id=farmer_id, user_id=user_id))
    user_name = find_user(user_id)
    farmer_name = find_user(farmer_id)
    result = db.session.execute(db.select(Chats))
    chats = result.scalars().all()
    user_id=user_id+10000
    farmer_id = farmer_id + 1000
    return render_template('farmer_chat.html',current_user=current_user,all_chats=chats,user=user_id,farmer=farmer_id,f_name=farmer_name,u_name=user_name)

@app.route('/negotiate1/<int:farmer_id>/<int:user_id>', methods=["GET", "POST"])
def negotiate_user(farmer_id,user_id):
    if request.method == "POST":
        message = request.form["message"]
        new_msg = Chats(
            farmer_id=farmer_id+1000,
            user_id=current_user.id+10000,
            posted_by=current_user.id,
            msg=message
        )
        db.session.add(new_msg)
        db.session.commit()
        return redirect(url_for('refresh1', farmer_id=farmer_id, user_id=user_id))
    user_name=find_user(user_id)
    farmer_name=find_user(farmer_id)
    result = db.session.execute(db.select(Chats))
    chats = result.scalars().all()
    user_id = user_id + 10000
    farmer_id = farmer_id + 1000
    print(user_name)
    return render_template('user_chat.html',current_user=current_user,all_chats=chats,farmer=farmer_id,user=user_id,f_name=farmer_name,u_name=user_name)

@app.route('/refresh/<int:farmer_id>/<int:user_id>', methods=["GET", "POST"])
def refresh(farmer_id,user_id):
    return redirect(url_for('negotiate', farmer_id=farmer_id, user_id=user_id))

@app.route('/refresh1/<int:farmer_id>/<int:user_id>', methods=["GET", "POST"])
def refresh1(farmer_id,user_id):
    return redirect(url_for('negotiate', farmer_id=farmer_id, user_id=user_id))
def generate_contract(contract):
    pdf = PDF()
    pdf.add_page()

    # Set background color
    pdf.set_fill_color(220, 220, 220)  # Light grey
    pdf.rect(x=0, y=0, w=210, h=297, style='F')  # Full page rectangle (A4 size)

    # Add logo
    logo_path = 'static/logo.png'
    logo_width = 150
    logo_height = 100
    pdf.image(logo_path, x=30, y=50, w=logo_width, h=logo_height, type='PNG')

    # Center and bold the contract title
    pdf.set_font("Helvetica", size=18, style='B')
    pdf.cell(0, 10, txt="Contract for Sale of Goods", ln=True, align='C')

    # Add a line break
    pdf.ln(10)
    pdf.set_y(20)

    # Set font for the contract content
    pdf.set_font("Helvetica", size=12)

    # Adding the contract content
    contract_template = f"""
    This Contract is made on the {contract.contract_date}, by and between:
    Farmer: {contract.farmer_name}
    Buyer: {contract.buyer_name}

    1. The Seller agrees to sell and the Buyer agrees to pay for a total amount of 
        Rs. {contract.total_amount} which includes 
        i)  price of goods Rs. {contract.goods_amount}
        ii) transportation cost Rs.{contract.transportation_amount}.
    2. The goods will be delivered to the following address: 
        Address: {contract.deliver_address}.
    3. The expected delivery date is {contract.delivery_date}.
    4. The Seller warrants that the goods are free from defects and conform to the 
        agreed specifications.
    5. The Buyer has 2 days from the delivery date to inspect the goods and notify 
        the Seller of any defects.
    6. This contract is governed by the laws of India, and disputes will be resolved 
        through arbitration in the city of the farmer. Amendments to this contract 
        must be made electronically and authenticated by both parties.
    7. This contract constitutes the entire agreement between the parties and may 
        only be amended electronically.

    Signatures:
    Farmer: {contract.farmer_name}
    Buyer: {contract.buyer_name}




            This is a auto-generated blank page, kindly ignore this page 
    """
    pdf.multi_cell(0, 10, txt=contract_template)

    # Save PDF
    pdf_file_path = os.path.join('static', 'contract.pdf')
    pdf.output(pdf_file_path)

@app.route('/admin', methods=["GET", "POST"])
def admin():
    result = db.session.execute(db.select(Confirmed_Contract))
    posts = result.scalars().all()

    return render_template("admin.html",all_posts=posts)

if __name__ == "__main__":
    app.run(debug=True)