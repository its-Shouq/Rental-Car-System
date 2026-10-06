#Two tabs:
#views/customer.py: customer home.
#- "Fleet": the fleet page with "Add to booking" (one car per booking).
#- "My booking": receipt after checkout, or an empty message, or the cart
#(car, dates, total, and buttons: Confirm rental, Update dates, Remove car).

import streamlit as st
import classes
#From theme.py we use:
#car_card_html -> the HTML of one car card
#flash         -> saves a short message that app.py shows as a small popup (toast)
#money         -> 60.5 becomes "60.50"
#sign_out      -> forgets the user and goes back to the welcome page
from theme import car_card_html, flash, money, sign_out
from views.fleet_filters import fleet_filters

#The page itself. app.py calls render(user) when the page is "customer_home".
#user is the logged-in Customer object (from the team's classes file).
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
    cars, rental = fleet_filters(show_dates=True) #show_dates=True -> customer: pick-up / return dates and the number of days
    catalog = classes.Cars(classes.available_cars)
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
                    if len(user.cart) == 1:
                        flash("You can only rent one car at a time.")
                    else:
                        user.add_to_cart(car, rental["days"])      # the team's method takes days
                        user.cart[0]["pickup"] = rental["pickup"]  # we also keep the dates
                        user.cart[0]["ret"] = rental["ret"]
                        flash("Car added to your booking.")
                    st.rerun()

            shown = shown + 1

# The "My booking" tab. Temporary text for now, we build it in the next step.
def booking_tab(user):
    st.write("My booking goes here")
            # increment the displayed cars count