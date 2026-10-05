# -*- coding: utf-8 -*-
"""
Entry point.  Run with:  python -m streamlit run app.py

How this file works:
Every time the user clicks a button or changes an input, Streamlit runs
app.py again from the first line to the last line.
So this file sets up the basics (page settings, saved state, CSS) and then
decides which page to show. It is the "router": it does not draw anything itself.
"""
#import streamlit library
import streamlit as st

# From our own theme.py file we need two helpers:
#   goto       -> changes the current page
#   inject_css -> adds our colors, cards and fonts to the page
from theme import goto, inject_css
from views import fleet, welcome

# Page settings: browser tab title, tab icon, and full-width layout.
# This must be the FIRST Streamlit command that runs in the file.
st.set_page_config(page_title="Wheels", page_icon="🚗", layout="wide")

# session_state is the app's memory. The file runs again on every click, so normal
# variables are reset each time, but values saved here are kept between runs.
ss = st.session_state

# Start on the welcome page, but only the first time.
# setdefault sets the value only if "page" does not exist yet, so later clicks
# do not send the user back to the welcome page.
ss.setdefault("page", "welcome")

# Add our CSS. It runs on every rerun because Streamlit redraws the page each time.
inject_css()


def coming_soon(user=None):
    """Pages we have not built yet."""
    st.info("This page is built in a later step.")
    st.button("\u2190 Back", on_click=goto, args=("welcome",))

# Page name -> the function that draws it.
# Note: welcome.render has no brackets. We are storing the function itself,
# not running it yet.
PAGES = {
    "welcome": welcome.render,
    "fleet": fleet.render,
    # next steps: "customer_auth", "admin_login", "customer_home", "admin_home"
}

PAGES.get(ss.page, coming_soon)(None)
