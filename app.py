import os
from flask import Flask, render_template, request, redirect, url_for, session
from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from dotenv import load_dotenv

load_dotenv(override=True)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/db-test")
def db_test():
    connection = get_db_connection()

    if connection:
        connection.close()
        return "SUCCESS: Flask is connected to MySQL!"

    return "ERROR: Database connection failed.", 500


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not username or not email or not password:
        return render_template(
            "register.html",
            message="All fields are required.",
            message_type="error"
        )

    if len(password) < 8:
        return render_template(
            "register.html",
            message="Password must contain at least 8 characters.",
            message_type="error"
        )

    if password != confirm_password:
        return render_template(
            "register.html",
            message="Passwords do not match.",
            message_type="error"
        )

    connection = get_db_connection()

    if connection is None:
        return "Database connection failed.", 500

    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            (email,)
        )

        if cursor.fetchone():
            return render_template(
                "register.html",
                message="This email is already registered.",
                message_type="error"
            )

        password_hash = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
            """,
            (username, email, password_hash)
        )

        connection.commit()

        return render_template(
            "register.html",
            message="Account created successfully!",
            message_type="success"
        )

    except mysql.connector.Error:
        connection.rollback()
        return render_template(
            "register.html",
            message="Something went wrong. Please try again.",
            message_type="error"
        ), 500

    finally:
        if cursor:
            cursor.close()
        connection.close()


if __name__ == "__main__":
    print("Starting AI Study Companion...")
    app.run(debug=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    connection = get_db_connection()

    if connection is None:
        return "Database connection failed.", 500

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, username, password_hash FROM users WHERE email = %s",
            (email,)
        )

        user = cursor.fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("home"))

        return render_template(
            "login.html",
            message="Invalid email or password.",
            message_type="error"
        )

    finally:
        if cursor:
            cursor.close()
        connection.close()


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))





