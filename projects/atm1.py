def check_balance(balance):
    print(f"Your current balance is ₹{balance}")
    return balance
def deposit(balance):
    amount = float(input("Enter amount to deposit: ₹"))
    balance += amount
    print(f"₹{amount} deposited successfully.")
    return balance
def withdraw(balance):
    amount = float(input("Enter amount to withdraw: ₹"))
    if amount > balance:
        print("Insufficient balance!")
    else:
        balance -= amount
        print(f"₹{amount} withdrawn successfully.")
    return balance
def atm():
    balance = 1000
    choice = ''
    print("""
--- ATM MENU ---
1. Check Balance
2. Deposit Money
3. Withdraw Money
4. Exit
""")
    choice = input("Choose an option:")

    if choice == '1':
        balance = check_balance(balance)
    elif choice == '2':
        balance = deposit(balance)
    elif choice == '3':
        balance = withdraw(balance)
    elif choice == '4':
        print("Thank you for using the ATM")
    else:
        print("Invalid option.Please try again.")
atm()
