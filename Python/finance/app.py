import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
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


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.context_processor
def injectcashbalance():
    cashbalance = getcashbalance()
    return dict(cashbalance=cashbalance)


def getcashbalance():
    if "user_id" in session:
        useridstr = str(session["user_id"])
        cash = db.execute("SELECT cash FROM users WHERE id = ?", useridstr)
        return cash

    else:
        cash = "Login to view Balance"
        return cash


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    useridstr = str(session["user_id"])
    inventorytable = "inventory_" + useridstr

    ownedstocks = db.execute("SELECT * FROM ?", inventorytable)
    for row in ownedstocks:
        symbol = row["symbol"]
        shares = row["shares"]
        stock = lookup(symbol)
        if stock:
            row["price"] = stock["price"]
            row["totalvalue"] = stock["price"] * shares
        else:
            return apology("Something went wrong", 400)

    # Get total value of balance + stocks
    useridstr = str(session["user_id"])
    totalbalancecash = db.execute("SELECT * FROM users WHERE id = ?", useridstr)
    totalbalance = float(totalbalancecash[0]["cash"])
    for row in ownedstocks:
        totalbalance += float(row["totalvalue"])

    return render_template(
        "index.html", ownedstocks=ownedstocks, totalbalance=totalbalance
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        shares = request.form.get("shares")

        if not request.form.get("symbol"):
            return apology("must provide a symbol", 400)

        if not request.form.get("shares"):
            return apology("must provide a share amount", 400)

        if stock == None or not stock:
            return apology("invalid symbol")

        if shares.isdigit() == False:
            return apology("Shares must be a positive number", 400)

        if request.form.get("shares") == "0":
            return apology("Shares must be a positive number", 400)

        else:
            # update user cash
            shares = int(request.form.get("shares"))
            hold = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            holdint = int(hold[0]["cash"])
            cost = int(float(stock["price"]) * shares)
            if holdint - cost < 0:
                return apology("you cant afford", 400)
            else:
                db.execute(
                    "UPDATE users SET cash = cash - ? WHERE id = ?",
                    stock["price"] * shares,
                    session["user_id"],
                )

                # cash = db.execute("SELECT cash FROM users WHERE id = ? ", session["user_id"])
                # round(cash)
                cash = shares
                useridstr = str(session["user_id"])
                historytable = "history_" + useridstr
                inventorytable = "inventory_" + useridstr

                # insert purchase into the history table
                db.execute(
                    f"INSERT INTO {historytable} (symbol, shares, pricepayed, balance) VALUES (?, ?, ?, ?)",
                    stock["symbol"],
                    shares,
                    stock["price"],
                    cash,
                )

                # insert new stocks in inventroy or uppdate if it exists

                istrue = db.execute(
                    f"SELECT * FROM {inventorytable} WHERE symbol = ?", symbol
                )
                if len(istrue) != 1:
                    db.execute(
                        f"INSERT INTO {inventorytable} (shares, symbol) VALUES (?, ?)",
                        shares,
                        symbol,
                    )
                else:
                    db.execute(
                        f"UPDATE {inventorytable} SET shares = shares + ? WHERE symbol = ?",
                        shares,
                        symbol,
                    )

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    useridstr = str(session["user_id"])
    tablename = "history_" + useridstr
    historys = db.execute(f"SELECT * FROM {tablename}")

    return render_template("history.html", historys=historys)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # create user database
        useridstr = str(session["user_id"])
        historytable = "history_" + useridstr
        inventorytable = "inventory_" + useridstr
        # creates history table
        db.execute(
            f"CREATE TABLE IF NOT EXISTS {historytable}(id INTEGER,symbol TEXT,shares INTEGER,buytime DATETIME,pricepayed INTEGER,balance INTEGER,PRIMARY KEY(id))"
        )
        # creates inventory table
        db.execute(
            f"CREATE TABLE IF NOT EXISTS {inventorytable}(id INTEGER,symbol TEXT,shares INTEGER,PRIMARY KEY(id))"
        )

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
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Empty field", 400)

        symbol = request.form.get("symbol")
        stock = lookup(symbol)

        if stock == None or not stock:
            return apology("invalid symbol")

        else:
            return render_template(
                "quoted.html",
                name=stock["name"],
                price=stock["price"],
                symbol=stock["symbol"],
            )
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) == 1:
            return apology("username already exists", 400)

        # Ensure username was submitted
        elif not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif password != confirmation:
            return apology("must provide two identical passwords", 400)

        else:
            # register user
            hashedpassword = generate_password_hash(
                password, method="pbkdf2", salt_length=16
            )
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username,
                hashedpassword,
            )
            return render_template("login.html")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    useridstr = str(session["user_id"])
    inventorytable = "inventory_" + useridstr
    historytable = "history_" + useridstr
    ownedstocks = db.execute("SELECT * FROM ?", inventorytable)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        shares = request.form.get("shares")

        if not request.form.get("symbol"):
            return apology("must provide a symbol", 400)

        if not request.form.get("shares"):
            return apology("must provide a share amount", 400)

        if request.form.get("shares") == "0":
            return apology("Shares must be a positive number", 400)

        if stock == None or not stock:
            return apology("invalid symbol")

        if shares.isdigit() == False:
            return apology("Shares must be a positive number", 400)

        else:
            ownedshares = db.execute(
                f"SELECT shares FROM {inventorytable} WHERE symbol = ?", symbol
            )
            shares = int(request.form.get("shares"))
            ownedsharescount = int(ownedshares[0]["shares"])
            if ownedsharescount < shares:
                return apology("You dont have that many shares", 400)
            else:
                db.execute(
                    f"UPDATE {inventorytable} SET shares = shares - ? WHERE symbol = ?",
                    shares,
                    symbol,
                )
                db.execute(
                    "UPDATE users SET cash = cash + ? WHERE id = ?",
                    stock["price"] * shares,
                    session["user_id"],
                )
                cash = -shares
                db.execute(
                    f"INSERT INTO {historytable} (symbol, shares, pricepayed, balance) VALUES (?, ?, ?, ?)",
                    stock["symbol"],
                    shares,
                    (stock["price"]),
                    cash,
                )

                return redirect("/")

    return render_template("sell.html", ownedstocks=ownedstocks)


@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("amount"):
            return apology("must provide Amount", 400)

        if request.form.get("amount") == "0":
            return apology("Amount must be a positive number", 400)

        if request.form.get("amount").isdigit() == False:
            return apology("Shares must be a positive number", 400)
        else:
            useridstr = str(session["user_id"])
            #

            intamount = int(request.form.get("amount"))
            db.execute(
                "UPDATE users SET cash = cash + ? WHERE id = ?", intamount, useridstr
            )

            return render_template("addcash.html")

    else:
        return render_template("addcash.html")


@app.route("/changepw", methods=["GET", "POST"])
@login_required
def changepw():
    """Get stock quote."""
    if request.method == "POST":
        useridstr = str(session["user_id"])
        oldpw = request.form.get("oldpw")
        newpw = request.form.get("newpw")

        # Ensure oldpw was submitted
        if not request.form.get("oldpw"):
            return apology("must provide old password", 403)

        # Ensure password was submitted
        elif not request.form.get("newpw"):
            return apology("must provide new password", 403)

        rows = db.execute("SELECT * FROM users WHERE id = ?", useridstr)

        # Ensure old password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], oldpw):
            return apology("invalid username and/or password", 403)

        else:
            hashedpassword = generate_password_hash(
                newpw, method="pbkdf2", salt_length=16
            )
            db.execute(
                "UPDATE users SET hash = ? WHERE id = ?", hashedpassword, useridstr
            )
            return redirect("/logout")

    else:
        return render_template("changepw.html")
