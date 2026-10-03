import streamlit as st
# need to import classes file

st.set_page_config(page_title="Car Rental System", layout="wide") #placeholder for now 
catalog = Cars(available_cars) #shows the catalog of cars available for renting 
st.title("Car Rental System") #title of the page, will be changed 

#st.write("Pick store location:")

st.divider()

f1, f2, f3 = st.columns(3) #filters for color, year, and price sorting
color_choice = f1.selectbox("Color", ["All"] + catalog.get_colors())
year_choice = f2.selectbox("Year", ["All"] + catalog.get_years())
sort_choice = f3.selectbox("Sort by price", ["Default", "Low to high", "High to low"])

display_cars = catalog.filter_cars(color_choice, year_choice)

if sort_choice == "Low to high":
    display_cars = catalog.sort_by_price(display_cars, True)
elif sort_choice == "High to low":
    display_cars = catalog.sort_by_price(display_cars, False)

filtered_available_cars = [car for car in display_cars if catalog.is_available(car)]

if len(filtered_available_cars) == 0:
    st.warning("No cars match your filters.")


availableCars = 0  # counts the displayed cars 
all_cars = catalog.get_all() # get all cars 
cols=st.columns(3)   # create 3 columns for displaying 
for car in display_cars: # loop through all cars 
    if catalog.is_available(car):
        col=cols[availableCars % 3]   # displays 3 cars per row
        box=col.container(border=True) # create a container for each car

        box.image(f"{car['id']}.jpg", use_container_width=True)
        box.subheader(car["model"], anchor=False) # displays the model 
        box.write(f"**Year:** {car['year']}")  # displays the year
        box.write(f"**Color:** {car['color']}")# displays the color
        box.write(f"**Price:** {car['price']} ⃁ per day") #displays the price
        box.success(f"Available: {car['quantity']}") #displays the quantity available (not sure)
        availableCars = availableCars + 1 # increment the available cars count 