# views/admin.py: admin home. def render(admin)
# Two tabs:
# - "Fleet": same cards as the customer, without booking.
# - "Manage fleet": "Add car" popup, a table of cars with Edit and Delete,
#   and a "Rentals" table (renter, car, dates, days, total).

import classes # import our file including admin class
import streamlit as st 

adm1 = classes.Admin("Wasan" , 22 , "xxxx@gmail.com" , "wsn41" , "12345")

st.title("Admin Page")

b1 , b2 , b3  , b4 = st.tabs(["Add a new car" , "Delete a car" , "Modify price" , "Modify quantity"])

with b1:
    with st.form("Add a car"):
        id1 = st.number_input("Car id: " , value = None )
        model = st.text_input("The model of the car: ")
        year = st.number_input("Year produced: " , value =None)
        price = st.number_input("The price of 1 day rent: " , value = None )
        color = st.text_input("Color of the car: ")
        quantity = st.number_input("The quantity ready to be rented: "  , value = None )

        submitted = st.form_submit_button("Submit")


        if submitted: 
            if not id1:
                st.error("ID required!")
            elif not model: 
                st.error("Model required!")
            elif not year :
                st.error("Year required!")
            elif not price: 
                st.error("Price required!")
            elif not color:
                st.error("Color required!")
            elif not quantity:
                st.error("Quantity required!")
            else:

                if int(id1) in [car['id'] for car in classes.available_cars]:
                    st.error("This car is already added to the list ...")
                else: 
                    adm1.add(id1 , model , year , price  , color , quantity)
                    st.success("The car has been saved successfuly!")

with b2: 
    with st.form("Delete car"):
        id2 = st.number_input("Enter the car id to delete: "  , value =None)

        submitted1 = st.form_submit_button("Submit")

        if submitted1:
            if not id2:
                st.error("ID required!")
            
            else:
    
                
                if int(id2) in [car['id'] for car in classes.available_cars]:
                    adm1.delete(id2)
                    st.success("Deleted successfully!")
                else: 
                    st.error("The car is not in the list ....")


with b3:
    with st.form("Modify price"):
        id3 = st.number_input("Enter the car id you wanna modify: " , value = None)
        new_price = st.number_input("Enter the new price : " , value = None)

        submitted2 = st.form_submit_button("Submit")

        if submitted2:
            if not id3:
                st.error("ID required!")
            elif not new_price:
                st.error("New price required!")
            else:
                if int(id3) in [car['id'] for car in classes.available_cars]:
                    adm1.modify_price(id3 , new_price)
                    st.success("change price successfully!")
                else:      
                    st.error("The car is not in the list ....")


with b4: 
    with st.form("Modify quantity"):

        id4 = st.number_input("Enter the car id:" , value = None)
        quantity1 =st.number_input("Enter the new quantity number: " , value = None)

        submitted3 = st.form_submit_button("submit")
        if submitted3:
            if not id4:
                st.error("ID required!")
            elif not quantity1: 
                st.error("New quantity required!")
            else:
    
                if int(id4) in [car['id'] for car in classes.available_cars]:
                    adm1.modify_quantity(id3 , quantity1)
                    st.success("change quantity successfully!")
                else:
                    st.error("The car is not in the list ....")
