from datetime import datetime
import os

admin_accounts = {}
user_accounts = {}
other_datas={}

# Function to find data from text files
def find_accounts_fun():
    global admin_accounts, user_accounts,other_datas
    if os.path.exists("admin_detail.txt"):
        with open("admin_detail.txt", "r") as file:
            for line in file:
                data = line.strip().split(',')
                admin_accounts[data[0]] = {
                    'name': data[1], 'password': data[2], 'balance': float(data[3]), 'transactions': [], 'role': 'admin'
                }
    if os.path.exists("user_detail.txt"):
        with open("user_detail.txt", "r") as file:
            for line in file:
                data = line.strip().split(',')
                user_accounts[data[0]] = {
                    'name': data[1], 'password': data[2], 'balance': float(data[3]), 'transactions': [], 'role': 'user'
                }

    if os.path.exists("other_details.txt") :
        with open("other_details.txt" ,"r") as file:
            for line in file:
                data = line.strip().split(',')  
                other_datas[data[0]]={
                    'email':data[1] , 'mobile':data[2] ,'address':data[3],'role':data[4]
                }

# Function to save data to text files
def save_accounts_fun():
    with open("admin_detail.txt", "w") as file:
        for acc, data in admin_accounts.items():
            file.write(f"{acc},{data['name']},{data['password']},{data['balance']}\n")
    
    with open("user_detail.txt", "w") as file:
        for acc, data in user_accounts.items():
            file.write(f"{acc},{data['name']},{data['password']},{data['balance']}\n")
 
    with open("other_details.txt", "w") as file:
        for acc, data in other_datas.items():
            file.write(f"{acc},{data['email']},{data['mobile']},{data['address']},{data['role']}\n")

            
# Function to authenticate user or admin
def pin_input_fun(acc_no):
    password = input("Enter your Password: ")
    if acc_no.startswith("A"):
        acc = admin_accounts.get(acc_no)
    else:
        acc = user_accounts.get(acc_no)
    return acc and acc['password'] == password

# Create admin account
def create_admin_account_fun():
    print("=== Admin Login ===")
    name = input("Create admin name: ")
    while True:
        password = input("Set password: ")
        if len(password)>=6 and len(password)<9:
            email=input("Enter your Email-address: ")
            break
        else:
            print("Password shoud have maximum 8 charactors.")
   
    while True:
        try:
            t_no_str=input("Enter your 10-degit mobile number start with 07: ")
            if t_no_str.isdigit() and len(t_no_str)==10 and t_no_str.startswith("07") :
                t_no=int(t_no_str)
                break
            else :
                print("Enter a 10-digit numbers starting with 07.")
        except ValueError:
            print("Numbers only!")           
    address=input("Enter your current address: ")
  
    a_id = f"A{len(admin_accounts) + 1:04d}"
    admin_accounts[a_id] = {'name': name, 'password': password, 'balance': 0, 'transactions': [], 'role': 'admin'}
    other_datas[a_id]={
        'email':email, 
         'mobile':t_no,
         'address':address,
         'role':"Staf"
         
    }
    print(f"Admin account created: {a_id}")    
    save_accounts_fun()
   
# Create user account
def create_user_account_fun():
    name = input("Enter account hloder's name: ")
    while True:
        password = input("Create a password: ")
        if len(password)>=6 and len(password)<9:
            email=input("Enter your Email-address: ")
            break
        else:
            print("Password shoud have maximum 8 charactors")
    while True:
        try:
            t_no_str=input("Enter your 10-degit mobile number start with 07: ")
            if t_no_str.isdigit() and len(t_no_str)==10 and t_no_str.startswith("07") :
                t_no=int(t_no_str)
                break
            else :
                print("Enter a 10-digit numbers starting with 07.")
        except ValueError:
            print("Numbers only!")           
    address=input("Enter your current address: ")
  
    while True:
        try:
            amount = float(input("Initial deposit: "))
            if amount < 0:
                print("Please enter positive amount")
            else:
                break
        except:
            print("Invalid amount")
            
    u_no = f"U{len(user_accounts) + 1:04d}"        
    user_accounts[u_no] = {
        'name': name, 'password': password, 'balance': amount,
        'transactions': [("Initial Deposit", amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "New account")], 'role': 'user'
    }
    other_datas[u_no]={
        'email':email, 
        'mobile':t_no,
        'address':address,
        'role':"Customer"
    }
    save_accounts_fun()
    print(f"User account created: {u_no}")

#All customer list    
def customer_list():
    for acc,data in user_accounts.items():
        print(f"{acc}:{data['name']}")

#check admin status
def check_status():
    acc=input("Enter Your Account no: ")
    if acc in admin_accounts:
        print(f"you are an Admin")
    elif acc in user_accounts:
        print(f"You are a Customer")
    else:
        print("Account no not found")    

# View all accounts function (admin use)
def view_all_accounts_fun():
    print("\n=== Admin Accounts ===")
    for acc, data in admin_accounts.items():
        print(f"{acc}  {data['name']}  LKR {data['balance']:.2f}  {data['role']}")
    
    print("\n=== User Accounts ===")
    for acc, data in user_accounts.items():
        print(f"{acc}  {data['name']}  LKR {data['balance']:.2f}  {data['role']}")

# View account details (user)
def view_my_account_fun():
    acc_no = input("Enter your account no: ")
    if acc_no in user_accounts and pin_input_fun(acc_no):
        acc = user_accounts[acc_no]
        print("----------------------------")
        print("      Full Details          ")
        print("----------------------------")
        print(f"Account Number: {acc_no}")
        print(f"Name: {acc['name']}")
        print(f"Balance: LKR {acc['balance']:.2f}")
        print(f"Role: {acc['role']}")
        print("----------------------------")
    else:
        print("Wrong account no or password.")

#Amount check function
def amount_input_fun(action="Process"):
    acc_no = input("Enter your account no: ")
    if acc_no in user_accounts and pin_input_fun(acc_no):
        while True:
            try:
                amount = float(input("Amount to deposit: "))
                if amount <= 0:
                    print("Enter a positive amount")
                else:
                    return acc_no ,amount
            except:
                print("Invalid amount.")
    else:
        print("Wrong account no or password.")     
        return None,None       

# Deposit money function
def deposit_money_fun():
        acc_no, amount=amount_input_fun("Deposit")
        if acc_no:
            desc = input("Description for deposit: ")
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user_accounts[acc_no]['balance'] += amount
            user_accounts[acc_no]['transactions'].append(("Deposit", amount, time, desc))
            save_accounts_fun()
            print("Deposit done.")
        else:pass    

# Withdraw money function
def withdraw_money_fun():
        while True :
            acc_no,amount=amount_input_fun("Withdraw")
            if acc_no:
                if amount< user_accounts[acc_no]['balance'] :
                    desc = input("Description for withdraw: ")
                    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    user_accounts[acc_no]['balance'] -= amount
                    user_accounts[acc_no]['transactions'].append(("Withdraw", amount, time, desc))
                    save_accounts_fun()
                    print("Withdraw done.")
                    break
                else: print("Insufficient balance!")    
            else:print("Account not found")
        
# Check balance function
def check_balance_fun():
    acc_no = input("Enter your account no: ")
    if acc_no in user_accounts and pin_input_fun(acc_no):
        print(f"Balance: LKR {user_accounts[acc_no]['balance']:.2f}")
    else:
        print("Wrong account no or password.")

# Transaction history function
def transaction_history_fun():
    acc_no = input("Enter your account no: ")
    if acc_no in user_accounts and pin_input_fun(acc_no):
        print(f"== {acc_no} Transactions History ==")
        for t in user_accounts[acc_no]['transactions']:
            print(f"{t[0]} LKR {t[1]:.2f}  {t[2]}  {t[3]}\t")
    else:
        print("Wrong account no or password.")


# Transfer money function 
def transfer_money_fun():
    from_acc = input("Enter your account no: ")
    if from_acc in user_accounts and pin_input_fun(from_acc):
        to_acc = input("To account no: ")
        if to_acc in user_accounts:
            try:
                amt = float(input("Enter Transfer amount: "))
                if amt <= 0 or user_accounts[from_acc]['balance'] < amt:
                    print("Invalid or insufficient funds.")
                    return
                desc = input("Description for transfer: ")
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user_accounts[from_acc]['balance'] -= amt
                user_accounts[to_acc]['balance'] += amt
                user_accounts[from_acc]['transactions'].append(("Transfer ", amt, time, desc))
                user_accounts[to_acc]['transactions'].append(("Received", amt, time, desc))
                save_accounts_fun()
                print("Transfer done.")
            except:
                print("Invalid amount.")
        else:
            print("Receiver account not found.")
    else:
        print("Wrong account no or password.")

#===================================================================Back function end=================================================================

#=====================================================================USER USE START==================================================================

#change password function
def change_password_fun():
    print("....If You Want Change Account password...\n")
    while True:
        print("--- change Password ---\n")
        print("1. change password")
        print("2. Forgot password")
        print("3. Logout")

        choice=input("choose (1-3): ")

        if choice == "1":
             uac_no=input("Enter your account no: ")
             if uac_no in user_accounts and pin_input_fun(uac_no):
                while True:
                    new_pass=input("Enter new password: ")
                    conform=input("Confirm your password: ")
                    if conform==new_pass:
                        user_accounts[uac_no]['password'] =new_pass
                        save_accounts_fun()
                        print("Password was change!\n")
                        break
                    else: 
                        print("Correct your password!")     
                            
             else:
                print("Wrong account no or password")   

        elif choice == "2":
            uac_no=input("Enter your account no: ")
            if uac_no in user_accounts:
                while True:
                    new_pass=input("Enter your new password: ")     
                    conform=input("Confirm your password: ")   
                    if conform == new_pass:
                        user_accounts[uac_no]['password'] =new_pass
                        save_accounts_fun()
                        print("Password was changed!\n")
                        break
                    else: 
                       print("Passwords do not match! Please try again.")     
            else:
                print("Account is not found")        

        elif choice =="3":
            break
        else:
            print("Invalid choice.")         


# Admin menu 
def admin_menu_fun(admin_id):
    print(f"Welcome {admin_accounts[admin_id]['name']}!")
    while True:
        print("\n=== Admin Menu ===")
        print("1. Create User Account")
        print("2. Create Admin Account")
        print("3. View All Accounts")
        print("4. Deposit Money")
        print("5. Withdraw Money")
        print("6. Transfer Money")
        print("7. Change Password")
        print("8. check customer list")
        print("9. Exit")

        choice = input("Choose (1-9): ")

        if choice == '1':
            create_user_account_fun()
        elif choice == '2':
            create_admin_account_fun()
        elif choice == '3':
            view_all_accounts_fun()
        elif choice == "4":
            deposit_money_fun()
        elif choice == "5":
            withdraw_money_fun()
        elif choice == "6":
            transfer_money_fun()   
        elif choice == "7":
            change_password_fun()   
        elif choice == "8":
            customer_list()            
        elif choice == '9':
            break
        else:
            print("Invalid Choice")

# Main menu for the system
def user_menu_fun(user_id):
    print(f"Welcome {user_accounts[user_id]['name']}!")
    while True:
        print("\n=== Mini Bank ===")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Balance Check")
        print("4. Transfer Money")
        print("5. View My Account")
        print("6. Transaction History")
        print("7. Change Password")
        print("8. Exit")

        choice = input("Choose (1-8): ")
          
        if choice == '1':
            deposit_money_fun()
        elif choice == '2':
            withdraw_money_fun()
        elif choice == '3':
            check_balance_fun()
        elif choice == '4':
            transfer_money_fun()
        elif choice == '5':
            view_my_account_fun()            
        elif choice == '6':
            transaction_history_fun()
        elif choice == "7":
            change_password_fun()    
        elif choice == '8':
            print("Thank you for using. Goodbye!")
            break
        else:
            print("Invalid choice")

#Main menu 
def main_menu_fun():
    find_accounts_fun()
    if not admin_accounts:
        print("Welcome to Our Unicome Mini Bank!")
        create_admin_account_fun()

    while True:
        print("\n--- MAIN MENU ---")
        print("1. Admin Login")
        print("2. User Login")
        print("3. Check Status")
        print("4. Exit")

        choice=input("Choose (1-4): ")

        if choice == "1":
              acc_no = input("Admin ID: ")
              if acc_no in admin_accounts and pin_input_fun(acc_no):
                   admin_menu_fun(acc_no)
              else:
                  print("Invalid admin ID or password.")
          
        elif choice == "2":
              uac_no = input("User Account No: ")
              if uac_no in user_accounts and pin_input_fun(uac_no):
                   user_menu_fun(uac_no)
              else:
                  print("Invalid admin ID or password.")
        elif choice == "3":
            check_status()          
            
        elif choice == "4":
            print("Thank you. Goodbye!")
            break
        else :
            print("Invalid choice")

main_menu_fun()

