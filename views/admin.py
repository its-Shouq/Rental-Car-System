# views/admin.py: admin home. def render(admin)
# Two tabs:
# - "Fleet": same cards as the customer, without booking.
# - "Manage fleet": "Add car" popup, a table of cars with Edit and Delete,
#   and a "Rentals" table (renter, car, dates, days, total).

import classes # import our file including admin class
import streamlit as st 

adm1 = classes.Admin("Wasan" , 22 , "xxxx@gmail.com" , "wsn41" , "12345")

st.title("Admin Page")

b1 , b2  = st.tabs(["Modify cars" ,  "Add a new car"])

with b1:
    for car in classes.available_cars: 
        col1 , col2 , col3 =st.columns([2.5 ,0.4 ,0.4], gap="xsmall" )
        with col1:
            st.write(f"id:{car['id']}  Model:{car['model']} Year:{car['year']} Color:{car['color']} Price:{car['price']} Quantity:{car['quantity']}")
        with col2:
            edit_button = st.button("Edit" , key =f"Edit_{car['id']}")
            if edit_button:
                st.session_state.editing_car = car['id']
        with col3: 
            delete_button = st.button("Delete" , key=f"Delete_{car['id']}")
            if delete_button: 
                adm1.delete(car['id'])
                st.rerun()
        if st.session_state.get("editing_car") ==car['id']:
            c1 , c2 = st.columns(2)
            with c1:
                new_price = st.number_input("New price: " , value = car['price'])
            with c2:
                new_quantity = st.number_input("New quantity" , value = car['quantity'])

            con1 , con2 = st.columns(2 , gap="xxsmall")
            with con1:
                if st.button("Save" , key= f"save_{car['id']}"):
                    
                    adm1.modify_price(car["id"] , new_price)
                    adm1.modify_quantity(car["id"] , new_quantity)
                    st.success("Done!!")

                    st.session_state.editing_car = None

                    st.rerun()
            with con2:
                if st.button("Cancel" , key = f"cancel_{car['id']}"):
                    st.session_state.editing_car = None
                    st.rerun()

with b2:
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
                    adm1.add(int(id1) , model , year , price  , color , int(quantity))
                    st.success("The car has been saved successfuly!")
                    st.rerun()
