import streamlit as st

cars = [ #a list of dictionaries representing cars that are avaible for renting
    {"id":1, "model":"Toyota Camry Se","year":2022,"color":"White", "price":60.50,"quantity":3},
    {"id":2, "model":"Honda Accord Hybrid","year":2020,"color":"Black" ,"price":80.75,"quantity":2},
    {"id":3, "model":"Hyundai Elantra","year":2023,"color":"Silver","price":60.75,"quantity":4},
    {"id":4, "model":"Kia Sportage", "year":2023,"color":"White","price":100.75,"quantity":1},
    {"id":5, "model":"Nissan Altima","year":2020,"color":"Blue","price":120.75,"quantity":2},
    {"id":6, "model":"Ford Explorer","year":2023,"color":"Red","price":170.00,"quantity":3},
    {"id":7, "model":"Chevrolet Tahoe","year":2021,"color":"Black","price":170.75,"quantity":2},
    {"id":8, "model":"Toyota Land Cruiser 300","year":2021,"color":"White","price":180.99,"quantity":1},
    {"id":9, "model":"Mazda CX-5", "year":2023, "color":"Black", "price":150.00,"quantity":3},
    {"id":10,"model":"GMC Yukon","year":2020, "color":"White","price":150.00,"quantity":2}
]

class Cars:  #temporary class to manage the car catalog until adding the user
    def __init__(self,cars): # constructor to initialize the class 
        self.cars=cars

    def get_all(self): #method to get all cars
        return self.cars

    def is_available(self,car): #method to check if a car is available
        return car["quantity"]>0

    def count_available(self): #method to count available cars
        x = 0 
        for car in self.cars:
            if self.is_available(car):
                x = x + 1
        return x

    def get_colors(self):
        colors = []
        for car in self.cars:
            if car["color"] not in colors:
                colors.append(car["color"])
        colors.sort()
        return colors

    def get_years(self):
        years = []
        for car in self.cars:
            if car["year"] not in years:
                years.append(car["year"])
        years.sort()
        return years

    def filter_cars(self, color, year):
        result = []
        for car in self.cars:
            color_match = color == "All" or car["color"] == color
            year_match = year == "All" or car["year"] == year
            if color_match and year_match:
                result.append(car)
        return result
    
    def get_price(self, car):
        return car["price"]

    def sort_by_price(self, car_list, ascending=True): #returns a new list, original stays untouched

        if ascending:
            return sorted(car_list, key=self.get_price)
        else:
            return sorted(car_list, key=self.get_price, reverse=True)


st.set_page_config(page_title="Car Rental System", layout="wide") #placeholder for now 
catalog = Cars(cars) #shows the catalog of cars available for renting 
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

available_cars = [car for car in display_cars if catalog.is_available(car)]

if len(available_cars) == 0:
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






