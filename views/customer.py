#Two tabs:
#views/customer.py: customer home.
#- "Fleet": the fleet page with "Add to booking" (one car per booking).
#- "My booking": receipt after checkout, or an empty message, or the cart
#(car, dates, total, and buttons: Confirm rental, Update dates, Remove car).

import streamlit as st
from datetime import date

import classes
#From theme.py we use:
#car_card_html -> the HTML of one car card
#flash         -> saves a short message that app.py shows as a small popup (toast)
#money         -> 60.5 becomes "60.50"
#sign_out      -> forgets the user and goes back to the welcome page

from theme import car_card_html, empty_html, flash, money, receipt_html, sign_out, summary_html
from views.fleet_filters import fleet_filters

#The page itself. app.py calls render(user) when the page is "customer_home".
#user is the logged-in Customer object.
def render(user):
    #Remember which tab is open (the first time it is the fleet tab)
    if "customer_tab" not in st.session_state:
        st.session_state["customer_tab"] = "fleet"
    #the dark bar on top
    navbar(user)

    #the main content: either the fleet or the booking
    if st.session_state["customer_tab"] == "fleet":
        fleet_tab(user)
    else:
        booking_tab(user)


# Button callback: change the open tab
def set_tab(name):
    st.session_state["customer_tab"] = name


def navbar(user):
    current = st.session_state["customer_tab"]

    # The active tab is a "primary" button, the other one is "tertiary" (the CSS styles both)
    fleet_kind = "tertiary"
    booking_kind = "tertiary"
    if current == "fleet":
        fleet_kind = "primary"
    else:
        booking_kind = "primary"

    #the top bar: logo, tabs, user name, sign out
    with st.container(key="navbar"):
        #six columns: logo, Fleet tab, My booking tab, space, user name, sign out
        c1, c2, c3, c4, c5, c6 = st.columns([1.3, 0.8, 1.5, 4.5, 1.3, 1.2],
                                            vertical_alignment="center")

        #the logo on the left
        c1.markdown('<span class="logo">Wheels</span>', unsafe_allow_html=True)
        #the two tabs: "Fleet" and "My booking"
        c2.button("Fleet", key="tab_fleet", type=fleet_kind,
                  on_click=set_tab, args=("fleet",))
        c3.button("My booking (" + str(len(user.cart)) + ")", key="tab_booking",
                  type=booking_kind, on_click=set_tab, args=("booking",))
        #the user name on the right
        c5.markdown('<div class="topname">' + user.name + '</div>', unsafe_allow_html=True)

        # sign_out (from theme.py) forgets the user and goes back to the welcome page
        c6.button("Sign out", key="signout", on_click=sign_out, use_container_width=True)


def fleet_tab(user):
    # The title, search bar and filters come from fleet.py.
    # We get back the list of cars and the chosen dates.
    cars, rental = fleet_filters() # return dates and the number of days
    catalog = classes.Cars(classes.available_cars) #call the Cars class to get the available cars
    # If no cars were found, we show a warning message.
    if len(cars) == 0:
        st.warning("No cars match your filters.")
        return

    # Text under the total price: "for 1 day" or "for 3 days"
    if rental["days"] == 1:
        days_text = "for 1 day"
    else:
        days_text = "for " + str(rental["days"]) + " days"

    shown = 0                                   # counts the displayed cars
    for car in cars:                            # loop through the cars
        if catalog.is_available(car):           # check if the car is available or not for the chosen dates
            if shown % 3 == 0:                  # start of a new row (3 cars per row)
                if shown > 0:
                    st.write("")                # space between the rows
                cols = st.columns(3, gap="large") #make 3 columns for the next 3 cars

            with cols[shown % 3]: #list of 3 columns, we fill the next one
                st.markdown(car_card_html(car), unsafe_allow_html=True)

                st.write("")
                # One row under the card: total price on the left, button on the right
                price_col, button_col = st.columns([1, 1.3], vertical_alignment="center")

                total = car["price"] * rental["days"]
                price_col.markdown('<div class="cardtotal"><strong>SAR ' + money(total) + '</strong>'
                                   '<span>' + days_text + '</span></div>',
                                   unsafe_allow_html=True)

                clicked = button_col.button("Add to booking", key="add_" + str(car["id"]),
                                            type="primary", use_container_width=True)
                if clicked:
                    ok, msg = user.add_to_cart(car, rental["pickup"], rental["ret"])
                    flash(msg)
                    if ok:
                        st.session_state["receipt"] = None     # a new booking: forget the old receipt
                    st.rerun()

            shown = shown + 1

#The "My booking" tab.
def booking_tab(user):
    if len(user.cart) == 1: #if there is a car in the cart, show it
        cart_view(user)
    elif st.session_state.get("receipt") is not None: #if the user has already checked out, show the receipt
        receipt_view(st.session_state["receipt"])
    else: #if the cart is empty and there is no receipt, show a message
        st.markdown(empty_html("No car in your booking yet",
                               "Pick one from the Fleet tab and choose your dates."),
                    unsafe_allow_html=True)
 
 
#Forget the dates saved in the two date boxes of the cart
# so the next car starts with its own dates)
def forget_cart_dates():
    st.session_state.pop("b_pickup", None)
    st.session_state.pop("b_return", None)
 
 
def cart_view(user):
    car = user.cart[0]                          # the car in the cart
    today = date.today()
 
    #the first time, the date boxes start with the dates saved in the cart
    if "b_pickup" not in st.session_state:
        st.session_state["b_pickup"] = car["pickup"]
    if "b_return" not in st.session_state:
        st.session_state["b_return"] = car["ret"]
 
    st.markdown('<div class="page-title">My booking</div>', unsafe_allow_html=True)
    #the page has two columns: the car card on the left, the dates and total on the right
    left, right = st.columns(2, gap="large")
    #the left column shows the car card
    with left:
        st.markdown(car_card_html(car), unsafe_allow_html=True)
    #the right column shows the dates, total and buttons
    with right:
        date_col1, date_col2 = st.columns(2)
        #the date boxes are initialized with the dates saved in the cart, but the user can change them.
        pickup = date_col1.date_input("Pick-up date", min_value=today,
                                      format="DD/MM/YYYY", key="b_pickup")
 
        #if the return date is now before the pick-up date, move it to the pick-up date
        if st.session_state["b_return"] < pickup:
            st.session_state["b_return"] = pickup
        #the return date cannot be before the pick-up date
        ret = date_col2.date_input("Return date", min_value=pickup,
                                   format="DD/MM/YYYY", key="b_return")
 
        #the days and the total come from classes.py and are calculated from the dates
        #on the screen, so they change as soon as the dates change (there is no update button)
        days = classes.rental_days(pickup, ret)
        total = classes.rental_total(car["price"], days)
        
        st.markdown(summary_html(car, days, total), unsafe_allow_html=True)
 
        st.write("")
        #the buttons: Confirm rental, Remove car
        confirm = st.button("Confirm rental", key="confirm_rental",
                            type="primary", use_container_width=True)
        remove = st.button("Remove car", key="remove_car", use_container_width=True)
        
        if confirm:
            user.modify_cart(pickup, ret)               # save the dates on the screen in the cart
            receipt = user.checkout()                   # updates the quantity and gives back the receipt
            st.session_state["receipt"] = receipt
            forget_cart_dates()
            st.rerun()
        #for the Remove button, we delete the car from the cart, forget the dates and show a flash message.
        if remove:
            ok, msg = user.delete_from_cart()
            forget_cart_dates()
            flash(msg)
            st.rerun()
 
 
def receipt_view(r):
    # Put the receipt in the middle column
    empty_left, middle, empty_right = st.columns([1, 2, 1])
 
    with middle:
        st.markdown(receipt_html(r), unsafe_allow_html=True)
 
        # Only changes the tab. The receipt stays, so My booking shows it again.
        st.button("Back to the fleet", key="back_to_fleet", on_click=set_tab, args=("fleet",))
 
