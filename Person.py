#import important libraries
#import streamlit as st 

# list of dictionaries that contains cars informations 
#id represents the car category 
available_cars = [{'id':1,'model':"BMW",'year':2026,'price':500,'color':"black",'quantity':3}] # store available cars
rented_cars = [] #store rented cars

#dictionary of taken usernames as a key and password as a value to avoid duplicates in usernames while sign up and check username while login
accounts = {"sara123": 123}

    #login method
def login(username,password):
    if username in accounts and accounts[username] == password :
     return "successfully login"
    else:
     return "your username or password is wrong"

# sort method that sort cars prices
sorted_cars = sorted(available_cars,key = lambda available_cars: available_cars['price'])

# a method that filter the cars by model or price or color 
def filter_by(model,price,color):
   filtered_values=[]
   for i in available_cars:
      if i["model"] == model or i["price"] == price or i["color"] == color:
        filtered_values.append(i)
   return filtered_values
      



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
          
             
          
       

    

# p = Person(input("Enter your name: "),int(input("Enter your age: ")),input("Enter your email: "),input("Enter your email: "),input("Enter your password: "))
# print(p.display_car_info())









