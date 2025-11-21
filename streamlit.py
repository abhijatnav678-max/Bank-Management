import streamlit as st
import json
import random
import string
from pathlib import Path

class Bank:
    database = "database.json"
    data = []

    # Load existing DB
    if Path(database).exists():
        with open(database) as fs:
            data = json.load(fs)
    else:
        with open(database, "w") as fs:
            json.dump([], fs)

    @classmethod
    def _update(cls):
        with open(cls.database, "w") as fs:
            json.dump(cls.data, fs, indent=4)

    @staticmethod
    def _account_number():
        alpha = random.choices(string.ascii_letters, k=5)
        digits = random.choices(string.digits, k=4)
        id_ = alpha + digits
        random.shuffle(id_)
        return "".join(id_)

    # Create Account
    @staticmethod
    def create_account(name, email, phone, pin):
        acc_no = Bank._account_number()
        new_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "pin": pin,
            "Account no.": acc_no,
            "Balance": 0
        }
        Bank.data.append(new_data)
        Bank._update()
        return acc_no

    @staticmethod
    def get_user(acc, pin):
        for user in Bank.data:
            if user["Account no."] == acc and user["pin"] == pin:
                return user
        return None

    # Deposit
    @staticmethod
    def deposit(acc, pin, amount):
        user = Bank.get_user(acc, pin)
        if not user:
            return False, "User not found"

        if amount <= 0:
            return False, "Invalid amount"
        if amount > 10000:
            return False, "Amount cannot exceed 10000"

        user["Balance"] += amount
        Bank._update()
        return True, "Amount Deposited"

    # Withdraw
    @staticmethod
    def withdraw(acc, pin, amount):
        user = Bank.get_user(acc, pin)
        if not user:
            return False, "User not found"

        if amount <= 0:
            return False, "Invalid amount"
        if amount > 10000:
            return False, "Amount cannot exceed 10000"
        if user["Balance"] < amount:
            return False, "Insufficient balance"

        user["Balance"] -= amount
        Bank._update()
        return True, "Amount Withdrawn"

    # Update details
    @staticmethod
    def update(acc, pin, name, email, phone, new_pin):
        user = Bank.get_user(acc, pin)
        if not user:
            return False, "User not found"
        
        if name: user["name"] = name
        if email: user["email"] = email
        if phone: user["phone"] = phone
        if new_pin: user["pin"] = new_pin

        Bank._update()
        return True, "Details Updated"

    # Delete
    @staticmethod
    def delete(acc, pin):
        user = Bank.get_user(acc, pin)
        if not user:
            return False, "User not found"

        Bank.data.remove(user)
        Bank._update()
        return True, "Account Deleted"


# -------------------------------
#       STREAMLIT UI
# -------------------------------

st.title("🏦 Simple Bank Application")

menu = st.sidebar.selectbox(
    "Select Action",
    ["Create Account", "Deposit Money", "Withdraw Money", "Account Details", "Update Details", "Delete Account"]
)

# CREATE ACCOUNT
if menu == "Create Account":
    st.header("Create a New Bank Account")
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    pin = st.text_input("PIN (4 digits)")

    if st.button("Create Account"):
        if len(pin) != 4 or not pin.isdigit():
            st.error("PIN must be 4 digits")
        elif len(phone) != 10 or not phone.isdigit():
            st.error("Phone number must be 10 digits")
        else:
            acc_no = Bank.create_account(name, email, phone, int(pin))
            st.success(f"Account created! Your Account Number: **{acc_no}**")

# DEPOSIT
elif menu == "Deposit Money":
    st.header("Deposit Money")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Deposit"):
        success, msg = Bank.deposit(acc, int(pin), amount)
        st.success(msg) if success else st.error(msg)

# WITHDRAW
elif menu == "Withdraw Money":
    st.header("Withdraw Money")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Withdraw"):
        success, msg = Bank.withdraw(acc, int(pin), amount)
        st.success(msg) if success else st.error(msg)

# DETAILS
elif menu == "Account Details":
    st.header("Account Details")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN")

    if st.button("Show Details"):
        user = Bank.get_user(acc, int(pin))
        if user:
            st.json(user)
        else:
            st.error("User not found")

# UPDATE DETAILS
elif menu == "Update Details":
    st.header("Update Account Details")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN")

    name = st.text_input("New Name (optional)")
    email = st.text_input("New Email (optional)")
    phone = st.text_input("New Phone (optional)")
    new_pin = st.text_input("New PIN (optional)")

    if st.button("Update"):
        success, msg = Bank.update(acc, int(pin), name, email, phone, new_pin)
        st.success(msg) if success else st.error(msg)

# DELETE ACCOUNT
elif menu == "Delete Account":
    st.header("Delete Account")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN")

    if st.button("Delete"):
        success, msg = Bank.delete(acc, int(pin))
        st.success(msg) if success else st.error(msg)
