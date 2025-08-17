from pymongo import MongoClient
import time as dt


db = client["library_db"]
users_col = db["users"]
books_col = db["books"]
bkstr_col = db["bookstores"]

def verify_email_val(email):
    return "@" in email and "." in email

def get_valid_email():
    while True:
        email = str(input("Your E-mail ID: "))
        if verify_email_val(email):
            return email
        else:
            print("Invalid email format. Please enter a valid email address (e.g., user@example.com).")

def get_valid_age():
    while True:
        age = int(input("Your Age: "))
        if 0 < age < 110:
            return age
        else:
            print("Invalid age. Please enter a positive integer.")

def get_valid_id():
    existing_ids = set()
    while True:
        ids = str(input("Choose an unique ID: "))
        if ids in existing_ids:
            print("ID already exists. Please choose a different ID.")
        else:
            if len(ids) > 0 and len(ids) < 16:
               existing_ids.add(ids)
               return ids
            else:
               print("Invalid ID. Please enter a unique ID between 1 and 15 characters.")

def add_record():
    full_name = str(input("Enter your Full Name: "))
    email = get_valid_email()
    age = get_valid_age()
    phone = int(input("Enter your Phone No: "))
    password = str(input("Enter your Password: "))
    user_id = get_valid_id()
    user_data = {
        "_id": user_id,
        "Name": full_name,
        "E-mail": email,
        "Age": age,
        "Phone No": phone,
        "Password": password,
        "Books": []
    }
    users_col.insert_one(user_data)
    print("Record added successfully.")

def view_records():
    user_id = str(input("Enter your ID: "))
    user_password = str(input("Enter your Password: "))
    user = users_col.find_one({"_id": user_id, "Password": user_password})
    if user:
        print(user)
    elif not users_col.find_one({"_id": user_id}):
        print("Invalid ID. Please try again.")
    else:
        print("Incorrect Password. Please try again.")

def del_record():
    print("Do you want to delete your library record? (Yes/No): ")
    delchoice = str(input()).strip().lower()
    if delchoice == "yes":
        user_id = str(input("Enter your ID: "))
        user_password = str(input("Enter your Password: "))
        user = users_col.find_one({"_id": user_id, "Password": user_password})
        if user:
            users_col.delete_one({"_id": user_id})
            print("Record deleted successfully.")
        elif not users_col.find_one({"_id": user_id}):
            print("Invalid ID. Please try again.")
        else:
            print("Incorrect Password. Please try again.")

def view_all_records():
    admin_id = str(input("Enter Admin ID: "))
    admin_pass = str(input("Enter Admin Password: "))
    if admin_id == "Sanjay M" and admin_pass == "kalvertersm0660":
        print("Admin access granted.")
        for user in users_col.find():
            print(user)
    else:
        print("You are not an admin.")

def update_record():
    print("Welcome to the Update Record Section")
    user_id = str(input("Enter your ID: "))
    user_password = str(input("Enter your Password: "))
    user = users_col.find_one({"_id": user_id, "Password": user_password})
    if user:
        print("What do you want to update in your library record? (Phone/Email/Name/Password/Age): ")
        upd_choice = str(input()).strip().lower()
        if upd_choice == "phone":
            new_phone = int(input("Enter new Phone No: "))
            users_col.update_one({"_id": user_id}, {"$set": {"Phone No": new_phone}})
            print("Phone No updated successfully.")
        elif upd_choice == "email":
            new_email = get_valid_email()
            users_col.update_one({"_id": user_id}, {"$set": {"E-mail": new_email}})
            print("E-mail ID updated successfully.")
        elif upd_choice == "name":
            new_name = str(input("Enter new Name: "))
            users_col.update_one({"_id": user_id}, {"$set": {"Name": new_name}})
            print("Name updated successfully.")
        elif upd_choice == "password":
            new_password = str(input("Enter new Password: "))
            users_col.update_one({"_id": user_id}, {"$set": {"Password": new_password}})
            print("Password updated successfully.")
        elif upd_choice == "age":
            new_age = get_valid_age()
            users_col.update_one({"_id": user_id}, {"$set": {"Age": new_age}})
            print("Age updated successfully.")
        else:
            print("Invalid update choice.")
    else:
        print("Invalid ID or Password. Please try again.")

def create_book_store():
    print("Welcome to the Book Store Creation Section! (Enter 0 to exit)\n")
    bkstr_name = input("Enter the Book Store Name/Exit: ")
    if bkstr_name == "0":
        dt.sleep(0.1)
        main()
    else:
        while True:
            bkstr_id = get_valid_id()
            bkstr_pass = str(input("Create the Book Store Password: "))
            bkstr_data = {
                "Name": bkstr_name,
                "_id": bkstr_id,
                "Password": bkstr_pass,
                "Books": []
            }
            bkstr_col.insert_one(bkstr_data)
            print("Book Store created successfully!")
            break

def add_books_bkstr():
    bkstr_id = str(input("Enter the Book Store ID: "))
    bkstr_pass = str(input("Enter the Book Store Password: "))
    bkstr = bkstr_col.find_one({"_id": bkstr_id, "Password": bkstr_pass})
    if bkstr:
        book_name = str(input("Enter the Book Name: "))
        book_author = str(input("Enter the Book Author: "))
        book_genre = str(input("Enter the Book Genre: "))
        book_price = float(input("Enter the Book Price: "))
        book_data = {
            "Name": book_name,
            "Author": book_author,
            "Genre": book_genre,
            "Price": book_price
        }
        # Add the book details (book_data) to the Books array of the bookstore
        bkstr_col.update_one({"_id": bkstr_id}, {"$push": {"Books": book_data}})
        print("Book added successfully!")
    else:
        print("Book Store not found.")

def visit_book_store():
    print("Welcome to the Book Store! (Enter 0 to exit)\n")
    bkstr_id = input("Enter the Book Store ID/Exit: ")
    bkstr = bkstr_col.find_one({"_id": bkstr_id})
    if bkstr:
        if bkstr.get("Books"):
            print("Books in this Book Store:")
            for book in bkstr["Books"]:
                print(f"[{book.get('Name', 'Unknown')}, {book.get('Price', 0)}, {book.get('Genre', 'Unknown')}]\n")

            input_choice = input("Do you want to add a book to your library record? (Yes/No): ").strip().lower()
            if input_choice == "yes":
                book_to_add = input("Enter the name of the book you want to add: ")
                if book_to_add in [book['Name'] for book in bkstr['Books']]:
                    user_id = str(input("Enter your ID: "))
                    user_pass = str(input("Enter your Password: "))
                    user = users_col.find_one({"_id": user_id, "Password": user_pass})
                    if user:
                        if "Books" not in user:
                            users_col.update_one({"_id": user_id}, {"$set": {"Books": [book_to_add]}})
                        else:
                            if book_to_add not in user.get("Books", []):
                                users_col.update_one({"_id": user_id}, {"$push": {"Books": book_to_add}})
                            else:
                                print("Book already added to your record.")
                                return
                        print(f"Book '{book_to_add}' added to your library record.")
                    else:
                        print("Invalid ID or Password.")
                else:
                    print("Book not found in this Book Store.")
        else:
            print("No books found in this Book Store.")
    else:
        print("Book Store not found.")
    if bkstr_id == "0":
        dt.sleep(0.1)
        main()

def view_book_store_names():
    print("Available Book Stores:")
    for bkstr in bkstr_col.find():
        print(f"Name: {bkstr['Name']}, ID: {bkstr['_id']}\n")
    dt.sleep(1.5)

def view_book_store():
    bkstr_id = input("Enter the Book Store ID: ")
    bkstr_pass = input("Enter the Book Store Password: ")
    bkstr = bkstr_col.find_one({"_id": bkstr_id, "Password": bkstr_pass})
    if bkstr:
        print("Book Store Details:")
        print(f"Name: {bkstr['Name']}\n")
        print(f"ID: {bkstr['_id']}\n")
        print(f"No. of Books: {len(bkstr['Books'])}\n")
        print(f"Books: {bkstr['Books']}\n")
    else:
        print("Book Store not found.")

def main():

    print("Welcome to the Library Management System!\n")

    while True:
      print("\n1) Add Record")
      print("2) View Record")
      print("3) Delete Record")
      print("4) View All Records")
      print("5) Update Record")
      print("6) View Book Store Names")
      print("7) Visit Book Store")
      print("8) Exit")
      print("9) Book Store Creator")

      choice = input("Enter your choice (1-9): ")
      if choice == "1":
          add_record()
          dt.sleep(1.5)
      elif choice == "2":
          view_records()
          dt.sleep(1.5)
      elif choice == "3":
          del_record()
          dt.sleep(1.5)
      elif choice == "4":
          view_all_records()
      elif choice == "5":
          update_record()
          dt.sleep(1.5)
      elif choice == "6":
          view_book_store_names()
      elif choice == "7":
          visit_book_store()
      elif choice == "8":
          dt.sleep(0.1)
          print("Exiting...")
          dt.sleep(0.5)
          print("Thank you for using the Library Management System!")
          break
      elif choice == "9":
          print("Initialising Book Store Creator...")
          dt.sleep(1)
          bkstr_main()
          break
      else:
          print("Invalid choice. Please try again.")

def bkstr_main():
    while True:
        print("\n1) Create Book Store")
        print("2) Add Books to Book Store")
        print("3) View Book Store")
        print("4) Exit\n")

        choice = input("Enter your choice (1-4): ")
        if choice == "1":
            create_book_store()
        elif choice == "2":
            add_books_bkstr()
        elif choice == "3":
            view_book_store()
        elif choice == "4":
            main()
            break
        else:
            print("Invalid choice. Please try again.")

main()