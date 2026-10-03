#First part of the code 
# list of dictionaries that contains cars informations , id represents the car category
available_cars = [ 
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
rented_cars = [] #store rented cars
#dictionary of taken usernames as a key and password as a value to avoid duplicates in usernames while sign up and check username while login
accounts = {"sara123": "123"}

#login method
def login(username,password):
    if username in accounts and accounts[username] == password :
     return "successfully login"
    else:
     return "your username or password is wrong"

#Second part of the code
#super class
class Person:
    #initiete attributes
    def __init__(self,name,age,email,username,password,license):
        self.name = name
        self.age= age
        self.email=email
        self.__password=password
        self.username=username
        self.license = license

    #method that display cars information 
    def display_car_info(self):
        return available_cars

    #sign-up method
    def sign_up(self):
       if self.username in accounts:
          return "user name already exist"
       if self.age >= 21:
          if self.license == True:
           accounts[self.username] = self.__password
           return "Sign up successful "
          else:
             return "You are illegal to drive "
       else:
          return "You are under legal age"

#Third part of the code,Subsclasses 
#Admin class
class Admin(Person):
#Define Admin class attributes.
  def __init__(self ,name,age,email,username,password,license):
    super().__init__(name,age,email,username,password,license)

#Enables the admin to add new cars to the system to be rented.
  def add(self ,id, model , year , price, color , quantity ):
    for car in available_cars:
      if car['model'] == model and car['year'] == year and car['color'] == color:
       return "already exists" 
    available_cars.append({'id':id , 'model': model , 'year' : year , 'price' : price ,'color': color, 'quantity' : quantity})

#Enables the admin to delete unwanted cars from the system premenantly.
  def delete(self , id):
    if id not in [car['id'] for car in available_cars]: 
      print("This car is already deleted or rented.")
    else: 
      for car in available_cars : 
        if car["id"] == id : 
          available_cars.remove(car)

#Enables the admin to modify the quantity of an existing car. 
  def modify_quantity(self , id , quantity ):
    if id not in [car['id'] for car in available_cars]:
      print("This car is already deleted or rented.")
    else:
      for car in available_cars:
        if car['id'] == id:
          car['quantity'] = quantity

#Enables the admin to modify the price of an existing car. 
  def modify_price(self , id , price):
    if id not in [car['id'] for car in available_cars]:
      print("This car is already deleted or rented.")
    else:
      for car in available_cars:
        if car['id'] == id:
          car['price'] = price


#Customer class(add commints)
class Customer(Person):
  def __init__(self,name,age,email,username,password, license,cart):
    super().__init__(name,age,email,username,password,license)
    self.cart = []


  def add_to_cart(self, car, days):

    if len(self.cart) >= 1:
      print("You can only rent one car.")
      return

    rental = car.copy()
    rental["days"] = days

    self.cart.append(rental)

    print("Car added to cart")


  def modify_cart(self, days):

    if not self.cart:
      print("Cart is empty.")
      return

    self.cart[0]["days"] = days

    print("Cart updated")


  def delete_from_cart(self):

    self.cart.clear()

    print("Car removed from cart.")


  def checkout(self):

    if not self.cart:
      print("Cart is empty.")
      return

    car = self.cart[0]

    total = car["price"] * car["days"]

    for available_car in available_cars:
      if available_car["id"] == car["id"]:
        available_car["quantity"] -= 1
        rented_cars.append(car)

        #if no cars are left
        if available_car["quantity"] ==0:
          available_cars.remove(available_car)
          
        break

    self.receipt(total)
    

    self.cart.clear()


  def receipt(self,total):
    car = self.cart[0]
    return f"Thank you!\n your receipt information: \n car model: {car['model']} \n Year: {car['year']} \n Color: {car['color']} \n Rented days: {car['days']} \n Total price: {total}"

#independent class that contains car's methods to manage the car
class Cars:  
# constructor to initialize the class 
    def __init__(self,cars):  
        self.cars=cars

#method to get all cars
    def get_all(self): 
        return self.cars
    
#method to check if a car is available
    def is_available(self,car): 
        return car["quantity"]>0

#method to count available cars
    def count_available(self): 
        x = 0 
        for car in self.cars:
            if self.is_available(car):
                x = x + 1
        return x

# mathod to get cars color
    def get_colors(self):
        colors = []
        for car in self.cars:
            if car["color"] not in colors:
                colors.append(car["color"])
        colors.sort()
        return colors

# mathod to get cars year
    def get_years(self):
        years = []
        for car in self.cars:
            if car["year"] not in years:
                years.append(car["year"])
        years.sort()
        return years

# mathod to filter the cars
    def filter_cars(self, color, year):
        result = []
        for car in self.cars:
            color_match = color == "All" or car["color"] == color
            year_match = year == "All" or car["year"] == year
            if color_match and year_match:
                result.append(car)
        return result

# mathod to sort cars price weather ascending or descinding
    def sort_by_price(self, car_list, ascending=True):
        if ascending:
          return sorted(car_list, key=lambda car: car["price"])
        else:
          return sorted(car_list, key=lambda car: car["price"], reverse=True)


#streamlit part on another file



          


