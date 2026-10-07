# -*- coding: utf-8 -*-
#views/fleet.py: the title, search bar and filters.
from datetime import date, timedelta #presente the date
import streamlit as st #from streamlit library
import classes

#fleet_filters draws the title, the search bar and the filters.
#it returns the cars to show (after the filters and the sort) and the chosen dates.
def fleet_filters():
    """
    Returns (cars, rental):
      cars   = the list of cars after the filters and the sort
      rental = {"pickup": date, "ret": date, "days": number}
    """
    today = date.today() #get the current date

# The page title
    st.markdown('<div class="page-title" style="margin:0 0 1rem 0">Fleet</div>', unsafe_allow_html=True)

        #default dates (only the first time): pick-up tomorrow, return 4 days from today
    if "pickup_date" not in st.session_state:
        st.session_state["pickup_date"] = today + timedelta(days=1)
    if "return_date" not in st.session_state:
        st.session_state["return_date"] = today + timedelta(days=4)

    cars_obj = classes.Cars(classes.available_cars)

    # ---- Search bar
    with st.container(key="searchbar"):
            #6 columns: pick-up, return, number of days, vertical line, search box, small empty space
            col1, col2, col3, col4, col5, col6 = st.columns([1.5, 1.5, 0.9, 0.2, 4.6, 0.01], vertical_alignment="bottom")
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
            #search box with a placeholder and an icon
            query = col5.text_input("Search", placeholder="Brand or model", key="car_query",
                                    icon=":material/search:")
            #the number of days is calculated, and shown in a small yellow box
            days = classes.rental_days(pickup, ret)
            rental = {"pickup": pickup, "ret": ret, "days": days}
            #display the number of days with singular/plural
            if days == 1:
                col3.markdown('<div class="daytag">1 day</div>', unsafe_allow_html=True)
            else:
                col3.markdown('<div class="daytag">' + str(days) + ' days</div>',
                              unsafe_allow_html=True)

    # ---- Filters: color buttons on the left, two dropdowns on the right
    col1, col2, col3 = st.columns([5.2, 1.2, 1.6], vertical_alignment="center")
    #colors pills
    color_options = ["All colors"] + cars_obj.get_colors()
    color = col1.pills("Color", color_options, default="All colors",
                       key="f_color", label_visibility="collapsed")

    #the year dropdown
    year_options = ["All years"]
    for y in cars_obj.get_years():
        year_options.append(str(y))
    year = col2.selectbox("Year", year_options, key="f_year", label_visibility="collapsed")
    #the sort dropdown
    order = col3.selectbox("Sort", ["Low to high price", "High to low price"], key="f_sort",
                           label_visibility="collapsed")

    # ---- Build the list with the team's methods
    if color is None or color == "All colors":
        color = "All"
    if year == "All years":
        year = "All"            # filter_cars from the team's file understands "All"
    else:
        year = int(year)

    cars = cars_obj.filter_cars(color, year)      # color and year
    cars = cars_obj.search(cars, query)           # search by model name
    cars = cars_obj.sort_by_price(cars, ascending=(order == "Low to high price"))   # sort by price

    return cars, rental
