import streamlit as st

from theme import inject_css
from views import customer

st.set_page_config(page_title="Wheels", page_icon="🚗", layout="wide")

ss = st.session_state
ss.setdefault("role", None)        # None (not logged in), "customer" or "admin". login.py and auth.py set it
ss.setdefault("receipt", None)
ss.setdefault("toast", None)
inject_css()

# Show a message after a button click (for example "Car added to your booking.")
if ss.toast:
    st.toast(ss.toast)
    ss.toast = None


# The customer home page. ss.customer is the Customer object made in login.py or auth.py
def customer_home():
    customer.render(ss.customer)


# Which pages the visitor can open depends on who is logged in.
# After log in, log out or sign up the page list changes, and Streamlit opens the
# first page of the new list (the one with default=True).
if ss.role == "customer":
    pages = [st.Page(customer_home, title="Wheels", url_path="customer", default=True)]
elif ss.role == "admin":
    pages = [st.Page("views/admin.py", title="Admin", default=True)]
else:
    pages = [st.Page("views/welcome.py", title="Welcome", default=True),
             st.Page("views/login.py", title="Log in"),
             st.Page("views/auth.py", title="Sign up")]

# position="hidden": no page menu in the sidebar, the buttons move between the pages
st.navigation(pages, position="hidden").run()
