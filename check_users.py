import sys
sys.path.insert(0, r'c:\Users\SV STORE\Desktop\UIT\Python\book_rental_project')
from db import fetch_all

users = fetch_all("SELECT Username, Password, Role, CustomerID FROM Users")
print("\nUsers in database:")
if users:
    for user in users:
        print(f"  Username: {user.Username}, Role: {user.Role}, Password: {user.Password}, CustomerID: {user.CustomerID}")
else:
    print("  No users found")
