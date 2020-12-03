import os
import requests

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from flask import Flask, session, render_template, redirect, request
from flask_sqlalchemy import sqlalchemy
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
db = sqlalchemy(app)

KEY = "UPxxlmKvhmOXvI07C5PQwA"


@app.route("/")
def index():
    # res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": "9781632168146"})
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        """ Assuming the username and password are already inserted """

        # Get the username and password the user inputted into the login form
        username = request.form.get("username")
        password = request.form.get("password")

        # Query database for username
        row = db.execute("SELECT * FROM users WHERE username = :username", 
                            {"username": username})

    else:
        return render_template("login.html")


    # if db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).rowcount == 0:
    #     return render_template("error.html", message="No such flight with that id.")
    # db.execute("INSERT INTO passengers (name, flight_id) VALUES (:name, :flight_id)",
    #         {"name": name, "flight_id": flight_id})
    # db.commit()

    # # User reached route via POST (as by submitting a form via POST)
    # if request.method == "POST":

    #     # Ensure username was submitted
    #     if not request.form.get("username"):
    #         return apology("must provide username", 403)

    #     # Ensure password was submitted
    #     elif not request.form.get("password"):
    #         return apology("must provide password", 403)

    #     # Query database for username
    #     rows = db.execute("SELECT * FROM users WHERE username = :username",
    #                       username=request.form.get("username"))

    #     # Ensure username exists and password is correct
    #     if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
    #         return apology("invalid username and/or password", 403)

    #     # Remember which user has logged in
    #     session["user_id"] = rows[0]["id"]

    #     # Redirect user to home page
    #     return redirect("/")

    # # User reached route via GET (as by clicking a link or via redirect)
    # else:
    #     return render_template("login.html")


@app.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    """Register user"""

    # Forget any user_id
    session.clear()

    # If user is trying to submit a form via POST
    if request.method == "POST":
        # Store the password entered by the user
        password = request.form.get("password")

    else:
        return render_template("sign-up.html")


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     """Register user"""

#     # Forget any user_id
#     session.clear()

#     # If user is trying to submit a form via POST
#     if request.method == "POST":

#         # Store the password entered by the user
#         password = request.form.get("password")
#         # Ensure a username is entered
#         if not request.form.get("username"):
#             return apology("Sorry you must provide a username", 403)

#         # Ensure a password is entered
#         elif not password:
#             return apology("Sorry you must provide a password", 403)

#         # Ensure the confiramtion password matches the first password
#         elif password != request.form.get("confirmation"):
#             return apology("Sorry your passwords don't match", 403)

#         # Ensure password is at least 8 characters long and contains at least one number
#         elif len(password) < 8:
#             return apology("Sorry, your password must be at least 8 characters long and contain a number", 403)

#         # Ensure the password contains at least one number
#         elif True:
#             flag = False

#             # Iterate over all the character in the password checking to see if there a number
#             for i in range(len(password)):
#                 try:
#                     charPassword = int(password[i])
#                     flag = True
#                     break
#                 except:
#                     continue

#             # Ensure the was at least one number before proceeding
#             if not flag:
#                 return apology("Sorry, your password must contain at least one number", 403)

#         # Hash password before inserting it into the database
#         db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", request.form.get("username"),
#             generate_password_hash(password))

#         # Get the current username registered with in order to attach a cookie to it
#         rows = db.execute("SELECT id FROM users WHERE username = ?", request.form.get("username"))

#         # Remember which user has logged in
#         session["user_id"] = rows[0]["id"]

#         # Redirect user to homepage
#         return index()

#     # If user got to route via get
#     else:
#         return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")