#import important libraries
#import streamlit as st 

# list of dictionaries that contains cars informations 
available_cars = [{'id':1,'model':"BMW",'year':2026,'price':500,'color':"black",'quantity':3}] # store available cars
rented_cars = [] #store rented cars

#set of taken usernames as a key and password as a value to avoid duplicates in usernames while sign up and check username while login
accounts = {"sara123": 123}

    #login method
def login(username,password):
    if username in accounts and accounts[username] == password :
     return "successfully login"
    else:
     return "your username or password is wrong"


#super class
class Person:
    #initiete attributes
    def __init__(self,name,age,email,username,password):
        self.name = name
        self.age= age
        self.email=email
        self.password=password
        self.username=username

    #method that display cars information 
    def display_car_info(self):
        return available_cars

    #sign-up method
    def sign_up(self):
       if self.username in accounts:
          return "user name already exist"
       
       accounts[self.username] = self.password
       return "Sign up successful "
    

p = Person(input("Enter your name: "),int(input("Enter your age: ")),input("Enter your email: "),input("Enter your email: "),input("Enter your password: "))
print(p.sign_up())







