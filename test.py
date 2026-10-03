import classes as c

customer = c.Customer("Sara",25, "sara@gmal ","sara25","1234",True, [])

print(customer.sign_up())
print(c.login("sara25", "1234"))

catalog = c.Cars(c.available_cars)

print(catalog.get_colors())
print(catalog.get_years())
print(catalog.count_available())

sorted_cars = catalog.sort_by_price(c.available_cars, True)

for car in sorted_cars:
    print(car["model"], car["price"])

car = c.available_cars[0]

customer.add_to_cart(car, 3)

print(customer.cart)

customer.modify_cart(5)
print(customer.cart)

print("Before:",c.available_cars[0]["quantity"])
customer.checkout()
print("After:", c.available_cars[0]["quantity"])
print("Rented:", c.rented_cars)
print("Cart:", customer.cart)
