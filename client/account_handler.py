def set_account_id(account_id: str):
    # Store the account_id in the local File, use Binary
    with open("account_id", "wb") as f:
        f.write(account_id.encode())
    return True

def get_account_id() -> str:
    # Read the account_id from the local File
    with open("account_id", "rb") as f:
        account_id = f.read().decode()
    return account_id
