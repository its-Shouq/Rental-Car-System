# views/admin.py: admin home. def render(admin)
# Two tabs:
#1- modify cars: list and modify cars exists in the system
#2- add a new car: add a new car to the list in the system


import classes # import our file including admin class
import streamlit as st 
from theme import inject_css, brand_panel , topbar , car_card_html

inject_css()# call the function to apply the theme

adm1 = classes.Admin("Manager" , 22 , "xxxx@gmail.com" , "admin" , "admin123") # initialize admin object

#Admin page title
st.markdown(
    '<div class="page-title">   Admin Dashboard</div>',
    unsafe_allow_html=True
)
# Tob bar of Wheels Website
topbar(adm1.name , "Admin")


#initialize the main two tabs (Modify cars and add a new car tabs)
b1 , b2  = st.tabs(["Modify cars" ,  "Add a new car"])
# modify cars tab
with b1:
    for car in classes.available_cars: 
        # Three columns: 1- for cars display 2- Edit button 3- Delete button
        col1 , col2 , col3 =st.columns([5 ,1 ,1], gap="xsmall" , vertical_alignment="center" )
        #print or display all cars in system
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

        #Edit button which enable the admin to modify price or quantity of any car in the system
        with col2:
            edit_button = st.button("Edit" , key =f"Edit_{car['id']}" , type = "primary" , use_container_width=True)
            if edit_button:
                st.session_state.editing_car = car['id'] # if press edit button start editing session
        #Delete button to delete the corresponding car from the system         
        with col3: 
            delete_button = st.button("Delete" , key=f"Delete_{car['id']}")
            if delete_button: 
                adm1.delete(car['id']) # if press delete button delete the car from the list using admin delete method
                st.rerun() #After deletion restart the session to view new changes

        #if editing car session start, two columns will appear: 1- modify price 2- modify quantity
        if st.session_state.get("editing_car") ==car['id']:
            c1 , c2 = st.columns([1,1] , gap="xxsmall")
            #modify the price of the corresponding car
            with c1:
                st.markdown('<div class="fleet-label"><b>New price:</b></div>', unsafe_allow_html=True)
                new_price = st.number_input("New price: " , value = car['price'], label_visibility="collapsed")
            #modify the quantity of the corresponding car
            with c2:
                st.markdown('<div class="fleet-label"><b>New quantity:</b></div>', unsafe_allow_html=True)
                new_quantity = st.number_input("New quantity" , value = car['quantity'], label_visibility="collapsed")
            # initialize four columns mainly use 2 columns for save and cance buttons
            left, con1 , con2 , right = st.columns([2 , 0.5, 0.5 ,2] , gap="xxsmall" )
            with con1:
                #Save button to save changes of the corresponding car
                if st.button("Save" , key= f"save_{car['id']}" , type = "primary", use_container_width=True ):
                    #modified using admin methods
                    adm1.modify_price(car["id"] , new_price) 
                    adm1.modify_quantity(car["id"] , new_quantity)
                    st.success("Done!!")

                    st.session_state.editing_car = None #stop the editing car session once saving changes

                    st.rerun() # restart the session
                    
            with con2:
                # cancel button to discard changes
                if st.button("Cancel" , key = f"cancel_{car['id']}" , use_container_width=True):
                    st.session_state.editing_car = None # stop the editing car session when discard changes
                    st.rerun() #restart the session

#Second tab to add a new car to the system
with b2:
    #form to fill the required information of the new car
    with st.form("Add a car"):
        #seperate the required information into two columns 
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

        # submit button to submit and send the form 
        submitted = st.form_submit_button("Submit" , key ="Submit" , type = "secondary" , use_container_width=True )


        if submitted: 
            #check if all required information are filled
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
                #check if car already in the system
                if int(id1) in [car['id'] for car in classes.available_cars]:
                    st.error("This car is already added to the list ...")
                else: 
                    #if not in the system it will be added to the system
                    adm1.add(int(id1) , model , year , price  , color , int(quantity)) #added using admin method
                    st.success("The car has been saved successfuly!")
                    st.rerun() #restart the session
