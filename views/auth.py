import streamlit as st
from classes import *
from theme import flash, inject_css, brand_panel, topbar, side_title, side_sub, field_error

st.set_page_config(page_title="Rental - Sign up", layout="wide")  # must be the first st command
inject_css()                                                      # each page loads the CSS itself


def email_error(email): # Returns an error message if the email looks wrong
    if email == "":
        return None
    if email.count("@") != 1:
        return "Email must have one @ sign."
    before, after = email.split("@")              # split into the part before and after @
    if before == "" or "." not in after or after.startswith(".") or after.endswith("."):
        return "Invalid Email"
    return None


def password_error(password, confirm): # Returns an error message if the two passwords are different
    if confirm == "":
        return None
    if password != confirm:
        return "Passwords do not match."
    return None


def signup_page():
    topbar()                                         # dark bar at the top with the logo and a Back button

    left, right = st.columns([1, 1.1], gap="large")  # split the page into 2 columns
    left.markdown(brand_panel("Welcome to Whelex",
                              "Please create an account to browse and rent a car."),
                  unsafe_allow_html=True)

    side_title("Sign up", right)
    side_sub("We require our customers to be at least 21 and have a driving license.", right)

    name = right.text_input("Full name")

    c1, c2 = right.columns([1, 2])                             # age and email
    age = c1.number_input("Age", min_value=0, max_value=90, step=1, value=21)
    email = c2.text_input("Email").strip()
    email_msg = email_error(email)                             # check the email right away
    if email_msg:
        field_error(email_msg, c2)

    username = right.text_input("Username")

    c3, c4 = right.columns(2)                                  # the two passwords
    password = c3.text_input("Password", type="password")
    confirm = c4.text_input("Confirm password", type="password")
    pass_msg = password_error(password, confirm)               # check the passwords right away
    if pass_msg:
        field_error(pass_msg, c4)

    license = right.radio("Valid driving license?", ["Yes", "No"], horizontal=True)

    has_errors = email_msg is not None or pass_msg is not None
    clicked = right.button("Create account", type="primary",
                           use_container_width=True, disabled=has_errors)

    if clicked:
        if not all([name.strip(), email, username.strip(), password, confirm]):
            right.error("Please fill in all fields.")
        else:
            customer = Customer(name.strip(), int(age), email, username.strip(),
                                password, license == "Yes", [])
            result = customer.sign_up()                        # checks username, age and license

            if result.startswith("Sign up successful"):
                st.session_state.username = customer.username
                st.session_state.role = "customer"
                st.session_state.customer = customer
                flash("Welcome, " + customer.name + "! Your account is ready.")
                st.rerun()                                     # app.py now opens the customer page
               
            else:
                right.error(result)

    right.caption("Already have an account?")
    if right.button("Log in instead", use_container_width=True):
        st.switch_page("views/login.py")                       # open the login page


signup_page()   # draw the page