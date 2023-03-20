import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    portfolio = db.execute(
        "SELECT symbol, name, shares, price, total FROM portfolio WHERE user_id = ?",
        session["user_id"],
    )

    # update current prices
    for i in range(len(portfolio)):
        symbol = portfolio[i]["symbol"]
        current_price = lookup(symbol)["price"]
        db.execute(
            "UPDATE portfolio SET price = ? WHERE user_id = ? AND symbol = ?",
            current_price,
            session["user_id"],
            symbol,
        )

    cash = round(db.execute("SELECT cash FROM users WHERE user_id = ?", session["user_id"])[
        0
    ]["cash"], 2)
    totalstock = round(db.execute(
        "SELECT SUM(total) FROM portfolio WHERE user_id = ?", session["user_id"]
    )[0]["SUM(total)"], 2)

    if len(portfolio) > 0:
        total = cash + totalstock
        return render_template(
            "index.html", portfolio=portfolio, cash=cash, total=total, message=""
        )
    return render_template("index.html", message="You don't own any stock")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Check if symbol exists
        try:
            symbol = lookup(request.form.get("symbol"))["symbol"]
        except TypeError:
            return apology("symbol doesn't exist", 400)

        # Check if shares is an integer
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("input a number for shares", 400)

        # Check if shares is > 0
        if not shares > 0:
            return apology("Can't buy negative amount of shares", 400)

        # Get user's cash and buy cost
        cash = db.execute(
            "SELECT cash FROM users WHERE user_id = ?", session["user_id"]
        )[0]["cash"]
        price = lookup(request.form.get("symbol"))["price"]
        cost = round((price * shares), 2)

        # Check if user has enough cash
        if cash < cost:
            return apology("Not enough cash", 400)

        # Subtract cost from user's cash
        db.execute(
            "UPDATE users SET cash = cash - ? WHERE user_id = ?",
            cost,
            session["user_id"],
        )

        # Record purchase in transactions table
        db.execute(
            "INSERT INTO transactions (user_id, symbol, cost, shares, type) VALUES (?, ?, ?, ?, ?)",
            session["user_id"],
            symbol,
            cost,
            shares,
            "buy",
        )

        # Insert new shares into user's portfolio
        if (
            len(
                db.execute(
                    "SELECT symbol FROM portfolio WHERE user_id = ? AND symbol = ?",
                    session["user_id"],
                    symbol,
                )
            )
            == 0
        ):
            name = lookup(request.form.get("symbol"))["name"]
            db.execute(
                "INSERT INTO portfolio (user_id, symbol, name, shares, price) VALUES (?, ?, ?, ?, ?)",
                session["user_id"],
                symbol,
                name,
                shares,
                price,
            )
        # Update user's portfolio if shares not in portfolio
        else:
            db.execute(
                "UPDATE portfolio SET shares = shares + ?, price = ? WHERE user_id = ? AND symbol = ?",
                shares,
                price,
                session["user_id"],
                symbol,
            )

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    elif request.method == "GET":
        return render_template("buy.html")


@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    """Let user change password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        current_password = request.form.get("current_password").strip()
        new_password = request.form.get("new_password").strip()
        confirmation = request.form.get("confirmation").strip()

        # Ensure current_password was submitted
        if not current_password:
            return apology("must provide current password", 400)

        # Ensure new_password was submitted
        elif not new_password:
            return apology("must provide new password", 400)

        # Ensure confirmation password was submitted
        elif not confirmation:
            return apology("must confirm new password", 400)

        # Ensure old and new password are different
        elif current_password == new_password:
            return apology("Old and new password are the same", 400)

        # Ensure password and confirmation password are the same
        elif confirmation != new_password:
            return apology("password confirmation failed", 400)

        # Ensure current_password and current_hash are the same
        current_hash = db.execute(
            "SELECT hash FROM users WHERE user_id = ?", session["user_id"]
        )[0]["hash"]
        if not check_password_hash(current_hash, current_password):
            return apology("wrong password", 400)

        # store new hash in database
        db.execute(
            "UPDATE users SET hash = ? WHERE user_id = ?",
            generate_password_hash(new_password),
            session["user_id"],
        )

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    elif request.method == "GET":
        return render_template("change_password.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    user_transactions = db.execute(
        "SELECT symbol, cost, shares, date, type FROM transactions WHERE user_id = ? ORDER BY date DESC",
        session["user_id"],
    )

    return render_template("history.html", transactions=user_transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

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
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Check if stock symbol exists
        try:
            symbol = lookup(request.form.get("symbol"))["symbol"]
        except TypeError:
            return apology("symbol doesn't exist", 400)

        name = lookup(request.form.get("symbol"))["name"]
        price = usd(lookup(request.form.get("symbol"))["price"])

        # Pass stock's info to and show quoted.html
        return render_template("quoted.html", symbol=symbol, name=name, price=price)

    # User reached route via GET (as by clicking a link or via redirect)
    elif request.method == "GET":
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        confirmation = request.form.get("confirmation").strip()

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure confirmation password was submitted
        elif not confirmation:
            return apology("must confirm password", 400)

        # Ensure password and confirmation password are the same
        elif confirmation != password:
            return apology("password confirmation failed", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username is not taken
        if len(rows) != 0:
            return apology("username already taken", 400)

        # Input user into database
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username,
            generate_password_hash(password),
        )

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    elif request.method == "GET":
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Check if symbol exists in user's portfolio
        symbol = request.form.get("symbol").upper()
        if (
            len(
                db.execute(
                    "SELECT symbol FROM portfolio WHERE user_id = ? AND symbol = ?",
                    session["user_id"],
                    symbol,
                )
            )
            == 0
        ):
            return apology("You don't own shares of that company", 400)

        # Check if shares is an integer
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("input a number for shares", 400)

        # Check if shares is > 0
        if not shares > 0:
            return apology("Can't sell less than 1 share", 400)

        # Check if user has enough shares
        shares_owned = db.execute(
            "SELECT shares FROM portfolio WHERE user_id = ? AND symbol = ?",
            session["user_id"],
            symbol,
        )[0]["shares"]
        if shares > shares_owned:
            return apology("Not enough shares to sell", 400)

        # Add profits to user's cash
        price = lookup(symbol)["price"]
        profit = round((shares * price), 2)
        db.execute(
            "UPDATE users SET cash = cash + ? WHERE user_id = ?",
            profit,
            session["user_id"],
        )

        # Record purchase in transactions table
        db.execute(
            "INSERT INTO transactions (user_id, symbol, cost, shares, type) VALUES (?, ?, ?, ?, ?)",
            session["user_id"],
            symbol,
            profit,
            shares,
            "sell",
        )

        # Remove shares from user's portfolio
        db.execute(
            "UPDATE portfolio SET shares = shares - ? WHERE user_id = ? AND symbol = ?",
            shares,
            session["user_id"],
            symbol,
        )

        # Remove stock from portfolio if no more shares owned
        shares_owned = db.execute(
            "SELECT shares FROM portfolio WHERE user_id = ? AND symbol = ?",
            session["user_id"],
            symbol,
        )[0]["shares"]
        if shares_owned < 1:
            db.execute(
                "DELETE FROM portfolio WHERE user_id = ? AND symbol = ?",
                session["user_id"],
                symbol,
            )

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    elif request.method == "GET":
        return render_template("sell.html")
