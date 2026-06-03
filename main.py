from customer import create_customer
from account import create_account
from account import view_account
from account import deposit
from account import withdraw
from account import check_balance
from account import view_transactions
from account import transfer_money
from account import login

while True:

    print("\n===== SMART BANK =====")
    print("1. Create Customer & Account")
    print("2. View Account")
    print("3. Deposit Money")
    print("4. Withdraw Money")
    print("5. Check Balance")
    print("6. View Transaction History")
    print("7. Transfer Money")
    print("8. Login")
    print("9. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        
        customer_id = create_customer()

        if customer_id is not None:
            
            create_account(customer_id)

    elif choice == "2":

        view_account()

    elif choice == "3":

        deposit()

    elif choice == "4":

        withdraw()

    elif choice == "5":
        
        check_balance()

    elif choice == "6":
        
        view_transactions()

    elif choice == "7":
        
        transfer_money()

    elif choice == "8":
        
        login()


    elif choice == "9":
        
        print("Thank You For Using SmartBank")
        break