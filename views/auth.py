import streamlit as st
from classes import *
from theme import flash, inject_css, brand_panel, topbar, side_title, side_sub, field_error

st.set_page_config(page_title="Rental - Sign up", layout="wide")  # must be the first st command
inject_css() # each page loads the CSS itself                                                     


def email_error(email): # Returns an error message if the email looks wrong
    if email == "":# If the user has not entered an email yet, nothing happen
        return None
    if email.count("@") != 1: # The email must contain one @ symbol.
        return "Email must have one @ sign."
    before, after = email.split("@") # split into the part before and after @
    if before == "" or "." not in after or after.startswith(".") or after.endswith("."):# Check that there is smth before the @, that there is a dot after the @, and that the dot is not at the start or end of the part after the @
        return "Invalid Email"
    return None #no email error found


def password_error(password, confirm): # Returns an error message if the two passwords are different
    if confirm == "":
        return None
    if password != confirm: # if passwords don't match 
        return "Passwords do not match."
    return None #the passwords match 


def signup_page():# function of the sign up page
    topbar()  # dark bar at the top with the logo and a Back button

    left, right = st.columns([1, 1.1], gap="large")  # split the page into 2 columns
    left.markdown(brand_panel("Welcome to Whelex",  # Display the welcome panel in the left column.
                              "Please create an account to browse and rent a car."),
                  unsafe_allow_html=True)

    side_title("Sign up", right) #Display the "Sign up" title
    side_sub("We require our customers to be at least 21 and have a driving license.", right)#note for the user

    name = right.text_input("Full name")#asks the user for their name

    c1, c2 = right.columns([1, 2])  # Create two columns for the age and email fields.                          
    age = c1.number_input("Age", min_value=0, max_value=90, step=1, value=21)# Ask for the user's age. ranges from 0 to 90
    email = c2.text_input("Email").strip()# strip() to removes spaces before and after the email.
    email_msg = email_error(email)  # call the function tocheck the email right away
    if email_msg: #display error under the email field.
        field_error(email_msg, c2)

    username = right.text_input("Username")#ask the user to choose a username

    c3, c4 = right.columns(2) # Create two columns for the password fields.                             
    password = c3.text_input("Password", type="password")# type="password" hides the characters while typing.
    confirm = c4.text_input("Confirm password", type="password")#to confirm the password
    pass_msg = password_error(password, confirm)  # Check whether the two passwords match.
    if pass_msg:#if error message display, put it under the confirm password field.
        field_error(pass_msg, c4)

    license = right.radio("Valid driving license?", ["Yes", "No"], horizontal=True)# checks if the customer has a valid driving license.

    has_errors = email_msg is not None or pass_msg is not None #if there is an error in email or password, the user wont be about to sign up
    clicked = right.button("Create account", type="primary",  # Create the account button (button is disabled if there are errors in the email or password fields).
                           use_container_width=True, disabled=has_errors)

    if clicked: # only runs when the user clicks "Create account".
        if not all([name.strip(), email, username.strip(), password, confirm]): #check all fields are filled and remove the space from the name and username
            right.error("Please fill in all fields.")
        else:
            customer = Customer(name.strip(), int(age), email, username.strip(),# Create a Customer object
                                password, license == "Yes", [])  # license == "Yes" converts to True/False
            result = customer.sign_up() # Call the Customer class's sign_up() method.

            if result.startswith("Sign up successful"):# if signed up successfully, save the username and role in Streamlit's session state, and rerun the app to open the customer page.
                st.session_state.username = customer.username 
                st.session_state.role = "customer" #saves the role
                st.session_state.customer = customer# Save the Customer object in the session.
                flash("Welcome, " + customer.name + "! Your account is ready.")# Display a welcome message to the new customer.
                st.rerun()   # Reload the application.then  app.py now opens the customer page
               
            else: # If sign-up failed, display the error returned by sign_up().
                right.error(result)

    right.caption("Already have an account?") # Display text asking users who already have an account to log in.
    if right.button("Log in instead", use_container_width=True):# Create a button to open the login page.
        st.switch_page("views/login.py") # open the login page


signup_page()  # Call the function to display the sign-up page.