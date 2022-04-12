import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///sneakers.db")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Ensure username was submitted, case sensitive
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Check if passwords match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Check if username is taken
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) > 0:
            return apology("username taken", 400)

        # Hash password and insert new user into users table
        hashvalue = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), hashvalue)

        # Redirect user to login page
        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/")
@login_required
def index():
    """Home Page"""
    return render_template("index.html")


@app.route("/releases")
@login_required
def releases():
    """Show releases"""

    # Query from database all the upcoming releases (greater than current date) under that user's ID.
    # Order by nearest release to farthest out.
    releases = db.execute("SELECT * FROM releases WHERE user_id = ? AND date >= CURRENT_DATE ORDER BY date ASC", session["user_id"])

    return render_template("releases.html", releases=releases)


@app.route("/addrelease", methods=["GET", "POST"])
@login_required
def addrelease():
    """Add release"""
    if request.method == "POST":

        # Ensure shoe brand was submitted
        if not request.form.get("brand"):
            return apology("must provide shoe brand", 400)

        # Ensure shoe model was submitted
        if not request.form.get("model"):
            return apology("must provide shoe model", 400)

        # Ensure shoe colorway was submitted
        if not request.form.get("colorway"):
            return apology("must provide shoe colorway", 400)

        # Ensure shoe release date was submitted
        if not request.form.get("date"):
            return apology("must provide release date", 400)

        # Make them all variables and upper case to limit user input error
        brand = request.form.get("brand").upper()
        model = request.form.get("model").upper()
        colorway = request.form.get("colorway").upper()
        date = request.form.get("date")

        # Insert the shoe release into the releases table in the database
        db.execute("INSERT INTO releases (user_id, brand, model, colorway, date) VALUES (?, ?, ?, ?, ?)", session["user_id"], brand, model, colorway, date)

        # Automatically redirect to releases page to show user it was added
        return redirect("/releases")

    else:
        return render_template("addrelease.html")


@app.route("/past")
@login_required
def past():
    """Show past releases"""

    # Query for user's releases that are less than current date AKA have already released.
    # Order by date descending so most recently passed release is at top.
    past = db.execute("SELECT * FROM releases WHERE user_id = ? AND date < CURRENT_DATE ORDER BY date DESC", session["user_id"])

    return render_template("past.html", past=past)


@app.route("/collection")
@login_required
def collection():
    """Show user collection"""

    # Query for user's owned sneakers, alphabetize by brand
    collection = db.execute("SELECT * FROM collection WHERE user_id = ? ORDER BY brand", session["user_id"])

    return render_template("collection.html", collection=collection)


@app.route("/addsneaker", methods=["GET", "POST"])
@login_required
def addsneaker():
    """Add sneaker to collection"""

    if request.method == "POST":

        # Ensure shoe brand was submitted
        if not request.form.get("brand"):
            return apology("must provide shoe brand", 400)

        # Ensure shoe model was submitted
        if not request.form.get("model"):
            return apology("must provide shoe model", 400)

        # Ensure shoe colorway was submitted
        if not request.form.get("colorway"):
            return apology("must provide shoe colorway", 400)

        # Make them all variables and upper case to limit user input error
        brand = request.form.get("brand").upper()
        model = request.form.get("model").upper()
        colorway = request.form.get("colorway").upper()

        # Insert the shoe release into the releases table in the database
        db.execute("INSERT INTO collection (user_id, brand, model, colorway) VALUES (?, ?, ?, ?)", session["user_id"], brand, model, colorway)

        return redirect ("/collection")

    else:
        return render_template("addsneaker.html")


@app.route("/community")
@login_required
def community():
    """Show other users' collection"""

    # Query for other user's collections and usernames, alphabetize by username then by shoe brand
    community = db.execute("SELECT username, brand, model, colorway FROM collection JOIN users ON collection.user_id = users.id WHERE user_id != ? ORDER BY username, brand", session["user_id"])

    return render_template("community.html", community=community)

@app.route("/info")
@login_required
def info():
    """Show links to sneaker release info sites"""
    return render_template("info.html")


@app.route("/shops")
@login_required
def shops():
    """Show links to shops"""
    return render_template("shops.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
