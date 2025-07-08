from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables
if os.environ.get("RENDER") != "true":
    load_dotenv("data.env")

# Setup Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "tempsecret")

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Signup form
class SignupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")

# Admin login form
class AdminLoginForm(FlaskForm):
    password = PasswordField("Admin Password", validators=[DataRequired()])
    submit = SubmitField("Login")

# Home route
@app.route("/")
def home():
    return redirect(url_for("signup"))

# Web signup form route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data  # In production, hash this!
        )
        db.session.add(new_user)
        db.session.commit()

        session["user"] = new_user.name
        session["email"] = new_user.email

        return redirect(url_for("profile"))
    return render_template("signup.html", form=form)

# API signup route (for Postman or frontend)
@app.route("/api/signup", methods=["POST"])
def api_signup():
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({"error": "Missing required fields"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 409

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Profile route
@app.route("/profile")
def profile():
    if "user" in session:
        return render_template("profile.html", name=session["user"], email=session["email"])
    else:
        return redirect(url_for("signup"))

# Admin login route
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        if form.password.data == os.getenv("ADMIN_PASSWORD", "admin123"):
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return "❌ Invalid admin password"
    return render_template("admin_login.html", form=form)

# Admin dashboard
@app.route("/admin")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    users = User.query.all()
    return render_template("admin_dashboard.html", users=users)

# Create DB tables
with app.app_context():
    db.create_all()

# Run the app
if __name__ == "__main__":
    app.run(debug=True)



#postgresql://postgres:password@localhost:5432/prometheus_db -> Original local