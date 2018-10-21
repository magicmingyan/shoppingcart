"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import melons
import customers

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print(melon)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.

    # The logic here will be something like:
    #
    # - get the cart dictionary from the session
    # - create a list to hold melon objects and a variable to hold the total
    #   cost of the order
    # - loop over the cart dictionary, and for each melon id:
    #    - get the corresponding Melon object
    #    - compute the total cost for that type of melon
    #    - add this to the order total
    #    - add quantity and total cost as attributes on the Melon object
    #    - add the Melon object to the list created above
    # - pass the total order cost and the list of Melon objects to the template
    #
    # Make sure your function can also handle the case wherein no cart has
    # been added to the session
    
    melon_list = []
    total_cost = 0
    if "cart" not in session:
        session["cart"] = {}

    for item in session["cart"]:
        melon = melons.get_by_id(item)
        melon.quantity = session["cart"][item]
        melon.totalprice = melon.quantity * melon.price
        melon_list.append(melon)
        total_cost += melon.totalprice

    return render_template("cart.html",
                    melon_list = melon_list,
                    total_cost = total_cost)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    # TODO: Finish shopping cart functionality

    # The logic here should be something like:
    #
    # - check if a "cart" exists in the session, and create one (an empty
    #   dictionary keyed to the string "cart") if not
    # - check if the desired melon id is the cart, and if not, put it in
    # - increment the count for that melon id by 1
    # - flash a success message
    # - redirect the user to the cart page
    if "cart" not in session:
        session["cart"] = {}

    if melon_id not in session["cart"]:
        session["cart"][melon_id] = 1
    else:
        session["cart"][melon_id] += 1

    flash("Successfully added melon to cart")
    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """
    email = request.form["email"]
    password = request.form["password"]

    if customers.get_by_email(email):
        if hash(password) == customers.get_by_email(email).hashed_password :
            session["logged_in_customer_email"] = email
            flash("Login successful")
            return redirect ('/melons')
        else:
            flash("Login unsuccessful")
            return redirect ('/login')
    else:
        flash("No customer with that email found.")
        return redirect('/login')


@app.route("/logout")
def process_logout():
    if "logged_in_customer_email" in session:
        session.pop("logged_in_customer_email", None)
    flash("Logout successfully")
    return redirect ('/melons')


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")

@app.route("/signup", methods = ["GET"])
def get_signup():
    """Sign up customer, add to customer object."""
    return render_template("signup.html")

@app.route("/signup", methods = ["POST"])
def signup():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    hashed_password = request.form["password"]

    new_customer = customers.Customer(first_name, last_name, email, hashed_password)

    customers.customers[email] = new_customer

    print(customers.customers)

    return redirect ('/melons')


if __name__ == "__main__":
    app.run(debug=True)
