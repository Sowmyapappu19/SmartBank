from db_connection import get_connection
import hashlib

def create_account(customer_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT MAX(account_no) FROM accounts"
    )

    result = cursor.fetchone()

    if result[0] is None:
        account_no = 100001
    else:
        account_no = result[0] + 1

    password = input("Create Password: ")
    hashed_password = hashlib.sha256(
        password.encode()
    ).hexdigest()

    account_type = input(
        "Enter Account Type (Savings/Current): "
    )

    query = """
    INSERT INTO accounts
    (account_no, customer_id, balance, password, account_type)
    VALUES(%s, %s, %s, %s, %s)
    """

    values = (
        account_no,
        customer_id,
        0,
        hashed_password,
        account_type
    )

    cursor.execute(query, values)

    connection.commit()

    print("\nAccount Created Successfully")
    print("Account Number:", account_no)

    connection.close()



def view_account():

    connection = get_connection()

    cursor = connection.cursor()

    account_no = int(input("Enter Account Number: "))

    query = """
    SELECT *
    FROM accounts
    WHERE account_no = %s
    """

    cursor.execute(query, (account_no,))

    account = cursor.fetchone()

    if account:

        print("\nAccount Details")
        print("----------------")
        print("Account Number:", account[0])
        print("Customer ID:", account[1])
        print("Balance:", account[2])
        print("Account Type:", account[4])

    else:
        print("Account Not Found")

    connection.close()


def deposit():

    try:

        connection = get_connection()

        cursor = connection.cursor()

        account_no = int(
            input("Enter Account Number: ")
        )

        amount = float(
            input("Enter Deposit Amount: ")
        )

        if amount <= 0:

            print("Amount Must Be Greater Than Zero")

            connection.close()

            return

        query = """
        UPDATE accounts
        SET balance = balance + %s
        WHERE account_no = %s
        """

        cursor.execute(
            query,
            (amount, account_no)
        )

        cursor.execute(
            """
            INSERT INTO transactions
            (account_no, transaction_type,
             amount, transaction_date)
            VALUES(%s, %s, %s, NOW())
            """,
            (
                account_no,
                "DEPOSIT",
                amount
            )
        )

        connection.commit()

        print(
            "\nAmount Deposited Successfully"
        )

        connection.close()

    except ValueError:

        print(
            "Invalid Input. Please Enter Numeric Values"
        )


    
def withdraw():

    try:

        connection = get_connection()

        cursor = connection.cursor()

        account_no = int(
            input("Enter Account Number: ")
        )

        amount = float(
            input("Enter Withdrawal Amount: ")
        )

        if amount <= 0:

            print("Amount Must Be Greater Than Zero")

            connection.close()

            return

        cursor.execute(
            """
            SELECT balance
            FROM accounts
            WHERE account_no = %s
            """,
            (account_no,)
        )

        result = cursor.fetchone()

        if result is None:

            print("Account Not Found")

            connection.close()

            return

        balance = result[0]

        if balance < amount:

            print("Insufficient Balance")

            connection.close()

            return

        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance - %s
            WHERE account_no = %s
            """,
            (amount, account_no)
        )

        cursor.execute(
            """
            INSERT INTO transactions
            (account_no, transaction_type,
             amount, transaction_date)
            VALUES(%s, %s, %s, NOW())
            """,
            (
                account_no,
                "WITHDRAW",
                amount
            )
        )

        connection.commit()

        print("\nWithdrawal Successful")

        connection.close()

    except ValueError:

        print(
            "Invalid Input. Please Enter Numeric Values"
        )    


def check_balance():

    try:

        connection = get_connection()

        cursor = connection.cursor()

        account_no = int(
            input("Enter Account Number: ")
        )

        cursor.execute(
            """
            SELECT balance
            FROM accounts
            WHERE account_no = %s
            """,
            (account_no,)
        )

        result = cursor.fetchone()

        if result:

            print(
                "\nCurrent Balance:",
                result[0]
            )

        else:

            print("Account Not Found")

        connection.close()

    except ValueError:

        print(
            "Account Number Must Be Numeric"
        )


def view_transactions():

    connection = get_connection()

    cursor = connection.cursor()

    account_no = int(input("Enter Account Number: "))

    cursor.execute(
        """
        SELECT transaction_type,
               amount,
               transaction_date
        FROM transactions
        WHERE account_no = %s
        ORDER BY transaction_date DESC
        """,
        (account_no,)
    )

    transactions = cursor.fetchall()

    if transactions:

        print("\nTransaction History")
        print("-" * 50)

        for transaction in transactions:

            print(
                transaction[0],
                "|",
                transaction[1],
                "|",
                transaction[2]
            )

    else:

        print("No Transactions Found")

    connection.close()


def transfer_money():

    try:

        connection = get_connection()

        cursor = connection.cursor()

        from_account = int(
            input("From Account Number: ")
        )

        to_account = int(
            input("To Account Number: ")
        )

        if from_account == to_account:

            print(
                "Cannot Transfer To Same Account"
            )

            connection.close()

            return

        amount = float(
            input("Enter Transfer Amount: ")
        )

        if amount <= 0:

            print(
                "Amount Must Be Greater Than Zero"
            )

            connection.close()

            return

        cursor.execute(
            """
            SELECT balance
            FROM accounts
            WHERE account_no = %s
            """,
            (from_account,)
        )

        sender = cursor.fetchone()

        if sender is None:

            print(
                "Sender Account Not Found"
            )

            connection.close()

            return

        cursor.execute(
            """
            SELECT account_no
            FROM accounts
            WHERE account_no = %s
            """,
            (to_account,)
        )

        receiver = cursor.fetchone()

        if receiver is None:

            print(
                "Receiver Account Not Found"
            )

            connection.close()

            return

        if sender[0] < amount:

            print(
                "Insufficient Balance"
            )

            connection.close()

            return

        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance - %s
            WHERE account_no = %s
            """,
            (amount, from_account)
        )

        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance + %s
            WHERE account_no = %s
            """,
            (amount, to_account)
        )

        cursor.execute(
            """
            INSERT INTO transactions
            (account_no, transaction_type,
             amount, transaction_date)
            VALUES(%s, %s, %s, NOW())
            """,
            (
                from_account,
                "TRANSFER_OUT",
                amount
            )
        )

        cursor.execute(
            """
            INSERT INTO transactions
            (account_no, transaction_type,
             amount, transaction_date)
            VALUES(%s, %s, %s, NOW())
            """,
            (
                to_account,
                "TRANSFER_IN",
                amount
            )
        )

        connection.commit()

        print("\nTransfer Successful")

        connection.close()

    except ValueError:

        print(
            "Invalid Input. Please Enter Numeric Values"
        )


def login():

    try:

        connection = get_connection()

        cursor = connection.cursor()

        account_no = int(
            input("Enter Account Number: ")
        )

        password = input(
            "Enter Password: "
        )

        hashed_password = hashlib.sha256(
            password.encode()
        ).hexdigest()

        cursor.execute(
            """
            SELECT *
            FROM accounts
            WHERE account_no = %s
            AND password = %s
            """,
            (
                account_no,
                hashed_password
            )
        )

        account = cursor.fetchone()

        if account:

            print("\nLogin Successful")

        else:

            print(
                "\nInvalid Account Number or Password"
            )

        connection.close()

    except ValueError:

        print(
            "Invalid Input. Please Enter Numeric Values"
        )