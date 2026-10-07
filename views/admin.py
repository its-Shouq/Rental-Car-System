# views/admin.py: admin home. def render(admin)
# Two tabs:
# - "Fleet": same cards as the customer, without booking.
# - "Manage fleet": "Add car" popup, a table of cars with Edit and Delete,
#   and a "Rentals" table (renter, car, dates, days, total).

import classes # import our file including admin class
import streamlit as st 
from theme import inject_css, brand_panel , topbar , car_card_html

inject_css()# call the function to apply the theme

adm1 = classes.Admin("Manager" , 22 , "xxxx@gmail.com" , "admin" , "admin123")

st.markdown(
    '<div class="page-title">   Admin Dashboard</div>',
    unsafe_allow_html=True
)

topbar(adm1.name , "Admin")




#st.markdown(brand_panel("Manage, add and edit your cars" , "" ),unsafe_allow_html = True) 



b1 , b2  = st.tabs(["Modify cars" ,  "Add a new car"])

with b1:
    for car in classes.available_cars: 
        col1 , col2 , col3 =st.columns([5 ,1 ,1], gap="xsmall" , vertical_alignment="center" )
        with col1:
            st.markdown(f"""
        <div class="fleet-row">
        <span><b>ID</b> <strong>{car['id']} |</strong></span>
        <span><b>Model</b> <strong>{car['model']} |</strong></span>
        <span><b>Year</b> <strong>{car['year']} |</strong></span>
        <span><b>Color</b> <strong>{car['color']} |</strong></span>
        <span><b>Price</b> <strong> {car['price']:.2f} SAR |</strong></span>
        <span><b>Quantity</b> <strong>{car['quantity']} |</strong></span>
        </div>
        """, unsafe_allow_html=True)
            #st.write(f"id:{car['id']}   Model:{car['model']}    Year:{car['year']}  Color:{car['color']}    Price:{car['price']}    Quantity:{car['quantity']}")
        with col2:
            edit_button = st.button("Edit" , key =f"Edit_{car['id']}" , type = "primary" , use_container_width=True)
            if edit_button:
                st.session_state.editing_car = car['id']
        with col3: 
            delete_button = st.button("Delete" , key=f"Delete_{car['id']}")
            if delete_button: 
                adm1.delete(car['id'])
                st.rerun()
        if st.session_state.get("editing_car") ==car['id']:
            c1 , c2 = st.columns([1,1] , gap="xxsmall")
            with c1:
                st.markdown('<div class="fleet-label"><b>New price:</b></div>', unsafe_allow_html=True)
                new_price = st.number_input("New price: " , value = car['price'], label_visibility="collapsed")
            with c2:
                st.markdown('<div class="fleet-label"><b>New quantity:</b></div>', unsafe_allow_html=True)
                new_quantity = st.number_input("New quantity" , value = car['quantity'], label_visibility="collapsed")

            left, con1 , con2 , right = st.columns([2 , 0.5, 0.5 ,2] , gap="xxsmall" )
            with con1:
                
                if st.button("Save" , key= f"save_{car['id']}" , type = "primary", use_container_width=True ):
                    
                    adm1.modify_price(car["id"] , new_price)
                    adm1.modify_quantity(car["id"] , new_quantity)
                    st.success("Done!!")

                    st.session_state.editing_car = None

                    st.rerun()
            with con2:
                
                if st.button("Cancel" , key = f"cancel_{car['id']}" , use_container_width=True):
                    st.session_state.editing_car = None
                    st.rerun()

with b2:
    with st.form("Add a car"):
        column1 , column2 = st.columns(2)
        
        with column1:
            st.markdown('<div class="fleet-label"><b>Car ID:</b></div>', unsafe_allow_html=True)
            id1 = st.number_input("Car ID:", value = None , label_visibility="collapsed" )

            st.markdown('<div class="fleet-label"><b>The model of the car: </b></div>', unsafe_allow_html=True)
            model = st.text_input("The model of the car: " , label_visibility="collapsed")

            st.markdown('<div class="fleet-label"><b>Year: </b></div>', unsafe_allow_html=True)
            year = st.number_input("Year produced: " , value =None , label_visibility="collapsed")
        with column2:
            st.markdown('<div class="fleet-label"><b>One day rent price: </b></div>', unsafe_allow_html=True)
            price = st.number_input("The price of 1 day rent: " , value = None, label_visibility="collapsed" )

            st.markdown('<div class="fleet-label"><b>Color:</b></div>', unsafe_allow_html=True)
            color = st.text_input("Color of the car: ", label_visibility="collapsed")

            st.markdown('<div class="fleet-label"><b>Quantity: </b></div>', unsafe_allow_html=True)
            quantity = st.number_input("The quantity ready to be rented: "  , value = None , label_visibility="collapsed")

        
        submitted = st.form_submit_button("Submit" , key ="Submit" , type = "secondary" , use_container_width=True )


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
