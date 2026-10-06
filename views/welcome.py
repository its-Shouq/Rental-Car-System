# views/welcome.py: welcome page. def render(user)
# - Left: dark brand panel. Right: "Ready to drive?" with buttons
#   "Log in", "Create account" (-> customer_auth) and "Just browse the cars" (-> fleet).
# - Small link at the bottom: "Are you an admin? Log in here" (-> admin_login).
import streamlit as st
from theme import inject_css, brand_panel, goto #import needed functions from css

inject_css() # call the function to apply the theme
left, right = st.columns(2) # split the page to left&right side

# start designing left side using brand_panel() and display it using st.markdown()
with left:
    st.markdown(brand_panel("Your car, ready when you are.","Choose a car, pick your dates, and confirm. One car per booking."),unsafe_allow_html=True)
# start designing right side
with right:
    # creating a coloumn that contains a spaces so we can make the content in the middle with a space from left and right 
    space1, content, space2 = st.columns([1, 8, 1])
    with content:
    # to create spaces until the med of the page
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.markdown('<div class="side-title">Ready to drive?</div>',unsafe_allow_html=True) # title style from theme class
        st.markdown('<div class="side-sub">Log in to book a car, or create an account in a minute.</div>',unsafe_allow_html=True) #side-sub style from theme class
        if st.button("Log in", type="primary", use_container_width=True):# create a log in button as a primary button 
          st.switch_page("views/login.py") # to navigate to login page 
        if st.button("Create account", use_container_width=True): # create "create account" button
         st.switch_page("views/auth.py") # to navigate to sign up page
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.markdown('<div style="text-align:center;">Are you an admin? <b>Log in here</b></div>',unsafe_allow_html=True) # admin log in , admin will click here to navegate to his page
    



