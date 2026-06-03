from db_connection import get_connection
import hashlib

connection = get_connection()
cursor = connection.cursor()

cursor.execute(
    """
    SELECT account_no, password
    FROM accounts
    """
)

accounts = cursor.fetchall()

for account in accounts:

    account_no = account[0]
    password = account[1]

    # Skip already hashed passwords
    if len(password) == 64:
        continue

    hashed_password = hashlib.sha256(
        password.encode()
    ).hexdigest()

    cursor.execute(
        """
        UPDATE accounts
        SET password = %s
        WHERE account_no = %s
        """,
        (hashed_password, account_no)
    )

connection.commit()

print("All passwords updated successfully")

connection.close()