# -*- coding: utf-8 -*-
# views/fleet.py: the title, search bar and filters (shared by customer and admin).
# It does NOT draw the car cards. Each page draws its own cards from the list it gets back.

from datetime import date, timedelta #presente the date
import streamlit as st #from streamlit library
import classes

#fleet_filters is used to filter the cars based on the user input. It returns a list of cars that match the filters.
#if true, it shows the date filters, otherwise it does not show the date filters.
#this is used for the admin page, which does not need to filter by date.
def fleet_filters(show_dates=True):
    """
    Draw the "Fleet" title, the search bar and the filters.

    show_dates=True  -> customer: pick-up / return dates and the number of days
    show_dates=False -> admin: only the text search

    Returns (cars, rental):
      cars   = the list of cars after the filters and the sort
      rental = {"pickup": date, "ret": date, "days": number}
               or None if the dates are not chosen yet (or show_dates is False)
    """

    today = date.today() #get the current date

        # default dates (only the first time): pick-up tomorrow, return 4 days from today
    if "pickup_date" not in st.session_state:
        st.session_state["pickup_date"] = today + timedelta(days=1)
    if "return_date" not in st.session_state:
        st.session_state["return_date"] = today + timedelta(days=4)

    cars_obj = classes.Cars(classes.available_cars)

    # Empty place for the title. We fill it at the end, when we know how many cars were found.
    title = st.empty()

    # ---- Search bar
    rental = None
    with st.container(key="searchbar"):
        if show_dates:
            # four columns: pick-up, return, number of days, search
            col1, col2, col3, col4, col5, col6 = st.columns([1.5, 1.5, 0.9, 0.2, 3.8, 0.8], vertical_alignment="bottom")

            pickup = col1.date_input("Pick-up date", min_value=today,
                                    format="DD/MM/YYYY", key="pickup_date")

            # if the return date is now before the pick-up date, move it to the pick-up date
            if st.session_state["return_date"] < pickup:
                st.session_state["return_date"] = pickup

            # the return date cannot be before the pick-up date
            ret = col2.date_input("Return date", min_value=pickup,
                                  format="DD/MM/YYYY", key="return_date")

            # light line between the days box and the search box
            col4.markdown('<div class="vline"></div>', unsafe_allow_html=True)

            query = col5.text_input("Search", placeholder="Brand or model", key="car_query",
                                    icon=":material/search:")

            days = classes.rental_days(pickup, ret)
            rental = {"pickup": pickup, "ret": ret, "days": days}
            if days == 1:
                col3.markdown('<div class="daytag">1 day</div>', unsafe_allow_html=True)
            else:
                col3.markdown('<div class="daytag">' + str(days) + ' days</div>',
                              unsafe_allow_html=True)
        else:
            query = st.text_input("Search", placeholder="Brand or model", key="car_query",
                                  icon=":material/search:")
    # ---- Filters: color buttons on the left, two dropdowns on the right
    col1, col2, col3 = st.columns([5.2, 1.2, 1.6], vertical_alignment="center")

    color_options = ["All colors"] + cars_obj.get_colors()
    color = col1.pills("Color", color_options, default="All colors",
                       key="f_color", label_visibility="collapsed")

    # The year list is text here ("All", "2020", ...), so we turn it back into a number below
    year_options = ["All"]
    for y in cars_obj.get_years():
        year_options.append(str(y))
    year = col2.selectbox("Year", year_options, key="f_year", label_visibility="collapsed")

    order = col3.selectbox("Sort", ["Low to high", "High to low"], key="f_sort",
                           label_visibility="collapsed")

    # ---- Build the list with the team's methods
    if color is None or color == "All colors":
        color = "All"
    if year != "All":
        year = int(year)

    cars = cars_obj.filter_cars(color, year)      # color and year
    cars = cars_obj.search(cars, query)           # search by model name
    cars = cars_obj.sort_by_price(cars, ascending=(order == "Low to high"))   # sort by price

    # ---- Fill the title now that we know how many cars we have
    if len(cars) == 1:
        count_text = "1 car available"
    else:
        count_text = str(len(cars)) + " cars available"
    title.markdown(
        '<div style="display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:1rem">'
        '<div class="page-title" style="margin:0">Fleet</div>'
        '<div style="color:#5E6A72;font-size:.9rem">' + count_text + '</div></div>',
        unsafe_allow_html=True)

    return cars, rental
