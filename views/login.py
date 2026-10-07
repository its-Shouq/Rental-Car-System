import streamlit as st
from classes import *
from theme import flash, inject_css, brand_panel, topbar, side_title, side_sub

st.set_page_config(page_title="Rental - Log in", layout="wide")  # must be the first st command
inject_css()                                                     # each page loads the CSS itself


def login_page():                                    # named login_page so it doesn't clash with login() from classes
    topbar()                                         # dark bar at the top with the logo and a Back button

    left, right = st.columns([1, 1.1], gap="large")  # split the page into 2 columns
    left.markdown(brand_panel("Welcome back", "Log in to browse and rent your next car."),
                  unsafe_allow_html=True)

    side_title("Log in", right)

    customer_tab, admin_tab = right.tabs(["Customer", "Admin"])

    # ---------------- Customer tab ----------------
    with customer_tab:
        side_sub("Enter your username and password.")
        username = st.text_input("Username", key="cust_user").strip()
        password = st.text_input("Password", type="password", key="cust_pass")

        if st.button("Log in", type="primary", use_container_width=True, key="cust_btn"):
            if username == "" or password == "":                  # a field is empty
                st.error("Please enter your username and password.")
            elif is_admin(username):                              # admins must use the Admin tab
                st.error("This is an admin account. Please use the Admin tab.")
            else:
                result = login(username, password)                # checks the accounts dictionary
                if result == "successfully login":
                    st.session_state.username = username          # remember who is logged in
                    st.session_state.role = "customer"
                    st.session_state.customer = Customer(username, 21, "", username, password, True, [])
                    flash("Welcome back, " + username + "!")    # small popup on the next page
                    st.rerun()                                    # app.py now opens the customer page
                    
                else:
                    st.error(result)                              # "your username or password is wrong"

        st.caption("Don't have an account?")
        if st.button("Sign up instead", use_container_width=True, key="to_signup"):
            st.switch_page("views/auth.py")                  # open the sign-up page

    # Admin tab 
    with admin_tab:
        side_sub("For staff only.")
        username = st.text_input("Admin username", key="admin_user").strip()
        password = st.text_input("Admin password", type="password", key="admin_pass")

        if st.button("Log in as admin", type="primary", use_container_width=True, key="admin_btn"):
            if username == "" or password == "":
                st.error("Please enter your username and password.")
            elif not is_admin(username):                          # only usernames in admins can log in here
                st.error("This is not an admin account.")
            else:
                result = login(username, password)
                if result == "successfully login":
                    st.session_state.username = username
                    st.session_state.role = "admin"
                    st.session_state.admin = Admin(username, 30, "", username, password)
                    flash("Welcome, " + username + " (admin)")
                    st.rerun()                                    # app.py now opens the admin page
                    
                else:
                    st.error(result)


login_page()   # draw the page