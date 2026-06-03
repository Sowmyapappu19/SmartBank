from db_connection import get_connection

def create_customer():

    connection = get_connection()

    cursor = connection.cursor()

    name = input("Enter Name: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone Number: ")

    cursor.execute(
        """
        SELECT *
        FROM customers
        WHERE email = %s OR phone = %s
        """,
        (email, phone)
    )

    existing_customer = cursor.fetchone()

    if existing_customer:

        print("\nCustomer with this Email or Phone Number already exists")

        connection.close()

        return None

    query = """
    INSERT INTO customers(name, email, phone)
    VALUES(%s, %s, %s)
    """

    values = (name, email, phone)

    cursor.execute(query, values)

    connection.commit()

    customer_id = cursor.lastrowid

    print("\nCustomer Created Successfully")
    print("Customer ID:", customer_id)

    connection.close()

    return customer_id