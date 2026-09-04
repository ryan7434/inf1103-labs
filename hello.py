print("=================")
print("Welcome here")
print("My first post")
print("=================")

username = input("Enter username: ")
age = int(input("Enter age: "))
category = input("Enter Content category: ")

print('\nInstagram Profile')
print('=================')
print('Username:', username)
print('Age:', age)
print('Category:', category)

if age>40 and category=="fun":
    print("You are too old what is fun for you??")